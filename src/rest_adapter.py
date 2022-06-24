import json
import time
from typing import List

import requests
import logging

from src.models.job_model import JobModel


class RESTAdapter:
    # PASSWORD = 'cVbr S0fX FM03 BAPe ylgH LpGt'
    # USERNAME = 'admin'
    PASSWORD = '6gP7 hmbq UsET twiT ezIW C8rR'
    USERNAME = 'adminnew'

    @staticmethod
    def _request_with_retry(request_function):
        RETRIES = 50
        retry = 0
        result = None
        while retry < RETRIES:
            try:
                result = request_function()
            except Exception as e:
                logging.error(
                    "Problem with REST request. . Exception: ",
                    e)
                logging.info("Perhaps lost internet connection. Retrying...")
                time.sleep(300)
                retry += 1
                continue
            break
        if retry == RETRIES:
            logging.error("Maximum retries reached. Aborting program")
            raise Exception("Maximum number of failed http requests reached")

        return result

    @staticmethod
    def upload_jobs(jobs: List[JobModel]):
        return RESTAdapter._request_with_retry(
            lambda: RESTAdapter._upload_jobs_once(jobs)
        )

    @staticmethod
    def delete_jobs(jobs: List[JobModel]):
        return RESTAdapter._request_with_retry(
            lambda: RESTAdapter._delete_jobs_once(jobs)
        )

    @staticmethod
    def _upload_jobs_once(jobs: List[JobModel]):
        jobs_dict = RESTAdapter._jobs_to_icf_valid_dict(jobs)
        r = requests.post(
            'https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs',
            auth=(RESTAdapter.USERNAME, RESTAdapter.PASSWORD),
            json=jobs_dict)
        logging.info("Website response after upload request:")
        logging.info(r.text)
        return r.json()

    @staticmethod
    def _delete_jobs_once(jobs: List[JobModel]):
        json = RESTAdapter._jobs_to_icf_valid_delete_dict(jobs)
        r = requests.delete(
            'https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs',
            auth=(RESTAdapter.USERNAME, RESTAdapter.PASSWORD),
            json=json)
        logging.info("Website response after delete request:")
        logging.info(r.text)
        return r.json()

    @staticmethod
    def _jobs_to_icf_valid_dict(jobs: List[JobModel]):
        """expecting a list of dictionaries"""
        return {
            "jobs":
                [job.as_dict() for job in jobs]
        }

    @staticmethod
    def _jobs_to_icf_valid_delete_dict(jobs: List[JobModel]):
        """creating a 'json' dict which contains only the job ids"""
        return {
            "jobs":
                [{'id': job.id} for job in jobs]
        }
