import requests
PASSWORD  = 'cVbr S0fX FM03 BAPe ylgH LpGt'
USERNAME = 'admin'


def upload_jobs(jobs):
    r = requests.post('https://internationalcareerfinder.com/wp-json/wp/v2/icf-jobs', auth=(USERNAME, PASSWORD),json=jobs)
    print(r.text)

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