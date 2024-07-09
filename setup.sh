#!/usr/bin/bash
python setup.py develop
sudo cp run.py /usr/bin/s3_utils
sudo chmod a+x /usr/bin/s3_utils