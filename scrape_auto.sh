#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate wcproduct
nordvpn connect
python ~/Workspace/job_scraper/main.py update_website
#echo "just debugging for the time being"
