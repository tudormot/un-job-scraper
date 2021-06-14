#!/bin/bash
#
#nordvpn connect
#echo "I am $USER, with uid $UID"
sudo -H -u tudor bash -c 'echo "I am $USER, with uid $UID"'
sudo -H -u tudor bash -c 'source /home/tudor/miniconda3/etc/profile.d/conda.sh ; conda activate job_scraping ; python /home/tudor/Workspace/job_scraper/main.py'

#echo "just debugging for the time being"
