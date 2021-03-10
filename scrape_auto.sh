#!/bin/bash
source /home/tudor/miniconda3/etc/profile.d/conda.sh
conda activate wcproduct
#nordvpn connect
echo "I am $USER, with uid $UID"
python /home/tudor/Workspace/job_scraper/main.py
#echo "just debugging for the time being"
