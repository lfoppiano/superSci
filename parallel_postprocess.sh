#!/bin/bash

echo "iop"
nohup python postprocess.py /data/workspace/archive/rawText/iop/ --output /data/workspace/archive/postProcessed/iop/ > nohup_iop  &
echo "aps"
nohup python postprocess.py /data/workspace/archive/rawText/aps/ --output /data/workspace/archive/postProcessed/aps/ > nohup_aps  &
echo "springer"
nohup python postprocess.py /data/workspace/archive/rawText/springer/ --output /data/workspace/archive/postProcessed/springer/ > nohup_springer  &
echo "elsevier"
nohup python postprocess.py /data/workspace/archive/rawText/elsevier/ --output /data/workspace/archive/postProcessed/elsevier/ > nohup_elsevier  &
echo "aip"
nohup python postprocess.py /data/workspace/archive/rawText/aip/ --output /data/workspace/archive/postProcessed/aip/ > nohup_aip &
echo "jjap" 
nohup python postprocess.py /data/workspace/archive/rawText/jjap/ --output /data/workspace/archive/postProcessed/jjap/ > nohup_jjap &
echo "wiley"
nohup python postprocess.py /data/workspace/archive/rawText/wiley/ --output /data/workspace/archive/postProcessed/wiley/ > nohup_wiley &
echo "rsc"
nohup python postprocess.py /data/workspace/archive/rawText/rsc/ --output /data/workspace/archive/postProcessed/rsc/ > nohup_rsc &
echo "acs"
nohup python postprocess.py /data/workspace/archive/rawText/acs/ --output /data/workspace/archive/postProcessed/acs/ > nohup_acs &
