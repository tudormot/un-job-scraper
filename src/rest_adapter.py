import time
import requests
import logging


class RESTAdapter:
    PASSWORD = 'cVbr S0fX FM03 BAPe ylgH LpGt'
    USERNAME = 'admin'

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
                    "Problem with REST request. Perhaps lost internet connection. Exception: ",
                    e)
                logging.info("Retrying...")
                time.sleep(300)
                retry += 1
                continue
            break
        if retry == RETRIES:
            logging.error("Maximum retries reached. Aborting program")
            raise Exception("Maximum number of failed http requests reached")

        return result

    @staticmethod
    def upload_jobs(jobs):
        RESTAdapter._request_with_retry(
            lambda: RESTAdapter._upload_jobs_once(jobs)
        )

    @staticmethod
    def delete_jobs(jobs):
        RESTAdapter._request_with_retry(
            lambda: RESTAdapter._delete_jobs_once(jobs)
        )


    @staticmethod
    def _upload_jobs_once(jobs):
        jobs_dict = RESTAdapter._jobs_to_dict(jobs)
        r = requests.post(
            'https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs',
            auth=(RESTAdapter.USERNAME, RESTAdapter.PASSWORD),
            json=jobs_dict)
        logging.info("Website response after upload request:")
        logging.info(r.text)
        r.json()


    @staticmethod
    def _delete_jobs_once(jobs):
        json = RESTAdapter._jobs_to_delete_dict(jobs)
        r = requests.delete(
            'https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs',
            auth=(RESTAdapter.USERNAME, RESTAdapter.PASSWORD),
            json=json)
        logging.info("Website response after delete request:")
        logging.info(r.text)
        return r.json()

    @staticmethod
    def _jobs_to_dict(jobs):
        """expecting a list of dictionaries"""
        return {
            "jobs":
                [job for job in jobs]
        }
    @staticmethod
    def _jobs_to_delete_dict(jobs):
        """creating a 'json' dict which contains only the job ids"""
        return {
            "jobs":
                [{'id': job['id']} for job in jobs]
        }
