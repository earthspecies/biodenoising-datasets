"""
Adapted from https://raw.githubusercontent.com/BirdVox/PCEN-SNR/master/src/pcen_snr.py under an MIT License
under MIT License
"""
import librosa
import numpy as np
import scipy
import scipy.signal


class ActivityDetector:
    '''
    This class implements the PCEN-SNR algorithm for detecting sound activity in a waveform.
    '''
    def __init__(
        self,
        n_mels=128,
        fmin=1000,
        fmax=11025,
        hop_length=512,
        gain=0.8,
        bias=10,
        power=0.25,
        pcen_time_constant=0.06,
        eps=1e-06,
        medfilt_time_constant=None,
        normalized=True,
        peak_threshold=0.4,
        activity_threshold=0.6,
    ):
        self.n_mels = n_mels
        self.fmin = fmin
        self.fmax = fmax
        self.hop_length = hop_length
        self.gain = gain
        self.bias = bias
        self.power = power
        self.pcen_time_constant = pcen_time_constant
        self.eps = eps
        self.medfilt_time_constant = medfilt_time_constant
        self.normalized = normalized
        self.peak_threshold = peak_threshold
        self.activity_threshold = activity_threshold

    def detect_activity(self, y, sr):
        """
        This function detects the segments of sound activity in a waveform and returns the start and
        end time of each sound event.

        Parameters
        ----------
        y : np.ndarray
            The input signal

        sr : number > 0 [scalar]
            The audio sampling rate

        Returns
        -------
        start_times : np.ndarray, nonnegative
            The start times of voice activities detected in signal y (seconds).

        end_times : np.ndarray, nonnegative
            The end times of voice activities detected in signal y (seconds).

        """
        if len(y.shape)>1 and y.shape[0] > 1:
            y = np.mean(y, axis=0)
        # 1. Compute mel-frequency spectrogram
        melspec = librosa.feature.melspectrogram(
            y=y,
            sr=sr,
            fmin=self.fmin,
            fmax=self.fmax,
            hop_length=self.hop_length,
            n_mels=self.n_mels,
        )

        # 2. Compute per-channel energy normalization (PCEN-SNR)
        pcen = librosa.core.pcen(
            melspec,
            sr=sr,
            gain=self.gain,
            bias=self.bias,
            power=self.power,
            hop_length=self.hop_length,
            time_constant=self.pcen_time_constant,
            eps=self.eps,
        )

        # 3. compute PCEN-SNR detection function
        pcen_snr = np.max(pcen, axis=0) - np.min(pcen, axis=0)
        pcen_snr = librosa.power_to_db(pcen_snr / np.median(pcen_snr))
        if self.normalized:
            pcen_snr = pcen_snr / np.max(pcen_snr)

        # 4. Apply median filtering.
        if self.medfilt_time_constant is not None:
            medfilt_hops = self.medfilt_time_constant * sr / self.hop_length
            kernel_size = max(1, 1 + 2 * round(medfilt_hops - 0.5))
            pcen_snr = scipy.signal.medfilt(pcen_snr, kernel_size=kernel_size)
    
        # 5. Extract active segments.
        activity, start, end = self.threshold_activity(
            pcen_snr, self.peak_threshold, self.activity_threshold
        )

        if len(start) > 0:
            # 6. Convert indices to seconds.
            start_times = [np.round(s * self.hop_length / sr, 3) for s in start]
            end_times = [np.round(e * self.hop_length / sr, 3) for e in end]
            start_times, end_times = self.join_events(start_times, end_times)
            start_times, end_times = self.enlarge_events(start_times, end_times)

            # zip start and end times
            start_end = np.array([[s, e] for s, e in zip(start_times, end_times)])
        else:
            start_end = np.array([[0., 0.]])

        return start_end

    def join_events(self, start_times, end_times, max_gap=4.0):
        # join events close apart in time
        index = 1
        while index < len(start_times):
            if (start_times[index] - end_times[index - 1]) < max_gap:
                end_times[index - 1] = end_times[index]
                del start_times[index]
                del end_times[index]
            else:
                index += 1
        return start_times, end_times

    def enlarge_events(self, start_times, end_times, min_len=1.0):
        # enlarge events
        index = 0
        while index < len(start_times):
            if (start_times[index] - end_times[index]) < min_len:
                start_times[index] = np.maximum(0.0, start_times[index] - min_len / 2)
                end_times[index] = end_times[index] + min_len / 2
            index += 1
        return start_times, end_times

    def threshold_activity(self, x, Tp, Ta):
        locs = scipy.signal.find_peaks(x, height=Tp)[0]
        if len(locs) > 1:
            y = (x > Ta) * 1
            act = np.diff(y)
            u = np.where(act == 1)[0]
            d = np.where(act == -1)[0]
            signal_length = len(x)
            if len(u) > 0 and len(d) > 0:
                if d[0] < u[0]:
                    u = np.insert(u, 0, 0)

                if d[-1] < u[-1]:
                    d = np.append(d, signal_length - 1)

                starts = []
                ends = []

                activity = np.zeros(
                    signal_length,
                )

                for candidate_up, candidate_down in zip(u, d):
                    candidate_segment = range(candidate_up, candidate_down)
                    peaks_in_segment = [x in candidate_segment for x in locs]
                    is_valid_candidate = np.any(peaks_in_segment)
                    if is_valid_candidate:
                        starts.append(candidate_up)
                        ends.append(candidate_down)
                        activity[candidate_segment] = 1.0
            else:
                starts = []
                ends = []
                activity = np.zeros(
                    len(x),
                )
        else:
            starts = []
            ends = []
            activity = np.zeros(
                len(x),
            )
        starts = np.array(starts)
        ends = np.array(ends)
        return activity, starts, ends
