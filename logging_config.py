import logging
import sys
import datetime
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


def config_log():
    if len(sys.argv)>1 and sys.argv[1] == 'log_to_file':
        filename = os.path.join(dir_path,'scraper.log')
        logging.basicConfig(level=logging.INFO, filename=filename, filemode='a', format='%(levelname)s - %(message)s')
        logging.info('##############')
        logging.info('Log recorded at: ' +str(datetime.datetime.now()))
        logging.info('##############')


    else:
        logging.basicConfig(level=logging.INFO)