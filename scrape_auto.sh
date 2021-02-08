#!/bin/bash
source /home/tudor/miniconda3/etc/profile.d/conda.sh
conda activate wcproduct
nordvpn connect
python /home/tudor/Workspace/job_scraper/main.py log_to_file
#echo "just debugging for the time being"
