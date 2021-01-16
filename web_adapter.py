import requests
import json

PASSWORD = 'cVbr S0fX FM03 BAPe ylgH LpGt'
USERNAME = 'admin'


def upload_jobs(jobs):

    json = jobs_to_dict(jobs)
    r = requests.post('https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs', auth=(USERNAME, PASSWORD),
                      json=json)
    print(r.text)
    return r.text

def upload_from_json(json):
    r = requests.post('https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs', auth=(USERNAME, PASSWORD),
                      json=json)
    print(r.text)
    return r.text


def delete_jobs():
    dummy_dict = {
        "jobs": [
            {
                "id": "1608592405428"
            },
            {
                "id": "1608589401659"
            },
        ]
    }
    r = requests.delete('https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs', auth=(USERNAME, PASSWORD),
                        json=dummy_dict)
    print(r.text)

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
