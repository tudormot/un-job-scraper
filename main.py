


import json

from icf_model import *









def save_jobs_as_JSON(job_list):
    dict = jobs_to_dict(job_list)
    with open('example.json', 'w') as outfile:
        json.dump(dict, outfile)

def jobs_to_dict(jobs):
    return {
        "jobs":
            [
                {
                    "title":job.title,
                    "organisation":job.organisation,
                    "country":job.country,
                    "city":job.city,
                    "office":job.office,
                    "grade":job.grade,
                    "closing_date":job.closing_date,
                    "tags":job.tags,
                    "original_job_link":job.original_job_link,
                    "extra_information":job.extra_information,
                    "id":job.id

                }
                for job in jobs
            ]
    }




def scrape_all_website_usecase():
    loader = icf_loader()
    model = loader.get_icf_model()


if __name__ == '__main__':
    # jobs = read_html_from_file()
    # save_jobs_as_JSON(jobs)
    # import codecs
    # data = json.load(codecs.open('example_v2.json', 'r', 'utf-8-sig'))
    # upload_jobs(data)

    # scrape_all_website_usecase()

