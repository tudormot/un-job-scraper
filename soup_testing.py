from scraping import *
from scrape_main_page import *
from web_adapter import *

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup

def test_learn_soup():
    soup = BeautifulSoup(html_doc, 'html.parser')
    print(soup.p)
    print(soup.shouldprintnone)

def test_re ():
    string = """I am a Consultant. I am also a consultant. find Consultants!"""
    pattern = 'Consultant|consultant'
    result = re.findall(pattern, string, re.IGNORECASE)
    print(result)

def test_re_2():
    i,c,p = 0,0,0
    text = 'Internbational is not considered intern. It is a consultancy though'
    pattern_internship = 'internship|intern[^a-z]'
    pattern_contractor = 'contractor|contract|consultancy'
    pattern_part_time = 'part time'

    c = len(re.findall(pattern_contractor, text, re.IGNORECASE))
    if c > 2:
        job_category = 'Contractor'
    else:
        i = len(re.findall(pattern_internship, text, re.IGNORECASE))
        if i > 3:
            job_category = 'Internship'

        else:
            p = len(re.findall(pattern_part_time, text, re.IGNORECASE))
            if p > 2:
                job_category = 'Part Time'
            else:
                job_category = 'Full Time '

    print("i,c,p = ",i,c,p)

def test_read_job_from_url():
    TEST_URL = "https://unjobs.org/vacancies/1610817517042"
    job = read_job_from_url(TEST_URL)
    print(job.as_dict())

def test_string_to_datetime():
    STRING = '2021-01-15T09:20:06Z'
    date = string_to_datetime(STRING)
    print(date)

def test_get_jobs_since_date():
    STRING = '2021-01-12T09:20:06Z'
    date = string_to_datetime(STRING)
    url_list, last_update_date = get_jobs_since_date(date)

    print(url_list)
    print("last_update_time: ",last_update_date)

def test_get_all_job_urls():
    url_list,last_update_date = get_all_job_urls()

    print(url_list)
    print("last_update_time: ",last_update_date)

def test_rest_api_incomplete_info():
    dummy_json = {
        'jobs' : [
            {
                "title": "dummy_jobszzz2",
                "original_job_link": "https://jobs.undp.org/cj_view_job.cfm?cur_job_id=96019",
                "extra_information": "blabla", # required
                "closing_date": "01.01.2025", # required
                "country" : None,
                "city:": None,
                "id": "12345"
            }
        ]
    }

    upload_from_json(dummy_json)


if __name__ == '__main__':
    # test_rest_api_incomplete_info()
    test_read_job_from_url()
    # test_re_2()
    # test_string_to_datetime()
    # test_get_jobs_since_date()
    # test_get_all_job_urls()