#!/bin/bash
#
#nordvpn connect
#echo "I am $USER, with uid $UID"
sudo -H -u tudor bash -c 'echo "I am $USER, with uid $UID"'
sudo -H -u tudor bash -c 'source /home/tudor/miniconda3/etc/profile.d/conda.sh ; conda activate un_scraping ; xvfb-run python3 /home/tudor/Workspace/un-job-scraper'

#echo "just debugging for the time being"
