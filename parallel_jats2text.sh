#!/bin/bash

echo "iop"
nohup python jats2text.py /data/workspace/archive/data/iop/ --output /data/workspace/archive/jats/iop/ > nohup_iop  &
echo "aps"
nohup python jats2text.py /data/workspace/archive/data/aps/ --output /data/workspace/archive/jats/aps/ > nohup_aps  &
echo "springer"
nohup python jats2text.py /data/workspace/archive/data/springer/ --output /data/workspace/archive/jats/springer/ > nohup_springer  &
echo "elsevier"
nohup python jats2text.py /data/workspace/archive/data/elsevier/ --output /data/workspace/archive/jats/elsevier/ > nohup_elsevier  &
echo "aip"
nohup python jats2text.py /data/workspace/archive/data/aip/ --output /data/workspace/archive/jats/aip/ > nohup_aip &
echo "jjap" 
nohup python jats2text.py /data/workspace/archive/data/jjap/ --output /data/workspace/archive/jats/jjap/ > nohup_jjap &
echo "wiley"
nohup python jats2text.py /data/workspace/archive/data/wiley/ --output /data/workspace/archive/jats/wiley/ > nohup_wiley &
echo "rsc"
nohup python jats2text.py /data/workspace/archive/data/rsc/ --output /data/workspace/archive/jats/rsc/ > nohup_rsc &
echo "acs"
nohup python jats2text.py /data/workspace/archive/data/acs/ --output /data/workspace/archive/jats/acs/ > nohup_acs &
