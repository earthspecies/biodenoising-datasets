mkdir -p ~/data/shipnoise/
aws --no-sign-request s3 sync s3://shipnoise-net/realtime_files/ ~/data/shipnoise
aws --no-sign-request s3 sync s3://acoustic-sandbox/2017_8_VesselsAndWavS/ ~/data/shipnoise/
