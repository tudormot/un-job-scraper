import requests
import json
import logging
from utils import fuzzy_delay

PASSWORD = 'cVbr S0fX FM03 BAPe ylgH LpGt'
USERNAME = 'admin'

def request_with_retry(jobs, request_function):
    RETRIES = 50
    retry = 0
    result = None
    while retry < RETRIES:
        try:
            result = request_function(jobs)
        except Exception as e:
            logging.error("Problem with REST request. Perhaps lost internet connection. Exception: ", e)
            logging.info("Retrying...")
            fuzzy_delay(300)
            retry+=1
            continue
        break
    if retry == RETRIES:
        logging.error("Maximum retries reached. Aborting program")
        raise Exception("Maximum number of failed http requests reached")

    return result


def upload_jobs(jobs):

    json = jobs_to_dict(jobs)
    r = requests.post('https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs', auth=(USERNAME, PASSWORD),
                      json=json)
    logging.info("Website response after upload request:")
    logging.info(r.text)
    return r.json()

# def upload_from_json(json):
#     #for testing purposes
#     r = requests.post('https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs', auth=(USERNAME, PASSWORD),
#                       json=json)
#     logging.info("Website response after upload request:")
#     logging.info(r.text)
#     return r.text


def delete_jobs(jobs):
    json = jobs_to_deletedict(jobs)

    r = requests.delete('https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs', auth=(USERNAME, PASSWORD),
                        json=json)
    logging.info("Website response after delete request:")
    logging.info(r.text)
    return r.json()

def save_jobs_as_JSON(job_list):
    dict = jobs_to_dict(job_list)
    with open('example.json', 'w') as outfile:
        json.dump(dict, outfile)

def jobs_to_dict(jobs):
    """expecting a list of dictionaries"""
    return {
        "jobs":
            [job for job in jobs]
    }
def jobs_to_deletedict(jobs):
    """creating a 'json' dict which contains only the job ids"""
    return {
        "jobs":
            [{'id':job['id']} for job in jobs]
    }
