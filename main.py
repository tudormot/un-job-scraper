import os
from bs4 import BeautifulSoup
from job_model import *
from selenium import webdriver
import pathlib
import time
import json


def _parse_string_for_date(closing_date_pretty):
    myhash = {
        'January' : '01',
        'February' : '02',
        'March' : '03',
        'April' : '04',
        'May' : '05',
        'June' : '06',
        'July' : '07',
        'August' : '08',
        'September' : '09',
        'October' : '10',
        'November' : '11',
        'December' : '12'
    }
    list = closing_date_pretty.split()
    return list[3] + '.' + myhash[list[4]] + '.' + list[5]




def job_from_html(html,id):
    raise Exception('deprecated')
    soup = BeautifulSoup(html, 'html.parser')
    job = JobModel()
    job.id = id
    job.title = soup.h2.string
    if job.title == None:
        print('ERROR parsing job title! TODO add in what link')

    contents = [x.contents for x in soup.find_all("li", class_="list-group-item dropdown-toggle")]
    contents.pop()  # drop twitter button information

    assert contents[0][0] == 'Organization:\n', 'ERROR parsing organization posting the job!'
    job.organisation = contents[0][1].string.strip('\n')
    assert contents[1][0] == 'Country:\n', 'ERROR parsing country of job!'
    job.country = contents[1][1].string.strip('\n')
    assert contents[2][0] == 'City:\n', 'ERROR parsing city of  job!'
    job.city = contents[2][1].string.strip('\n')
    assert contents[3][0] == 'Office:\n', 'ERROR parsing office of job!'
    job.office = contents[3][1].string.strip('\n')

    #get closing date
    tag = soup.find("div", class_='job'+job.id)
    iter = tag.children
    _ = iter.__next__()
    t = iter.__next__()
    job.closing_date_pretty = t.string
    job.closing_date = _parse_string_for_date(job.closing_date_pretty)
    print(job.closing_date)

    #get tags
    job.tags = [x.a.string for x in soup.find_all("div", class_="md-chip md-chip-raised md-chip-hover")[1:]]
    print(job.tags)

    return job

def read_html_from_file():
    offline_jobs_dir= "offline_jobs"
    job_list = []
    for file in os.listdir(offline_jobs_dir)[:4]: #TODO limit to 1 is temp

        uri = pathlib.Path(os.path.abspath(offline_jobs_dir + '/' + file)).as_uri()

        driver = webdriver.Chrome('/snap/bin/chromium.chromedriver')
        driver.get(uri)

        html = driver.page_source
        id = file.split('.')[0]

        soup = BeautifulSoup(html, 'html.parser')
        job = JobModel()
        job.id = id
        job.title = soup.h2.string
        if job.title == None:
            print('ERROR parsing job title! TODO add in what link')

        contents = [x.contents for x in soup.find_all("li", class_="list-group-item dropdown-toggle")]
        contents.pop()  # drop twitter button information

        assert contents[0][0] == 'Organization:\n', 'ERROR parsing organization posting the job!'
        job.organisation = contents[0][1].string.strip('\n')
        assert contents[1][0] == 'Country:\n', 'ERROR parsing country of job!'
        job.country = contents[1][1].string.strip('\n')
        assert contents[2][0] == 'City:\n', 'ERROR parsing city of  job!'
        job.city = contents[2][1].string.strip('\n')
        assert contents[3][0] == 'Office:\n', 'ERROR parsing office of job!'
        job.office = contents[3][1].string.strip('\n')
        try:
            assert contents[4][0] == 'Grade:\n', 'ERROR parsing grade of job!'
            job.grade = contents[4][1].string.strip('\n')
        except:
            job.grade = None

        # get closing date
        tag = soup.find("div", class_='job' + job.id)
        iter = tag.children
        _ = iter.__next__()
        t = iter.__next__()
        job.closing_date_pretty = t.string
        job.closing_date = _parse_string_for_date(job.closing_date_pretty)
        #print(job.closing_date)

        # get tags
        job.tags = [x.a.string for x in soup.find_all("div", class_="md-chip md-chip-raised md-chip-hover")[1:]]
        #print(job.tags)

        #get original job link: TODO: button needs to be pressed twice only when using html from file take that into account
        button = driver.find_element_by_id("more-info-button")
        time.sleep(2)  # 2s
        button.click()
        time.sleep(2) #2s
        button = driver.find_element_by_id("more-info-button")
        button.click()
        time.sleep(2)
        job.original_job_link = driver.current_url
        #print('debug, original linK: ', job.original_job_link)

        #get text content
        text_tag= soup.find("div", class_='t' + job.id)
        #print('text_tag is', text_tag)

        # bmore = text_tag.find('div',class_='bmore')
        # bmore.decompose()

        ads = text_tag.find_all('ins', class_='adsbygoogle')
        #print('number of adsbygoogle found: ', len(ads))
        for ad in ads:
            ad.decompose()
        tag_buttons = text_tag.find_all("div",class_ = 'md-chips')
        #print('number of tag containers found: ', len(tag_buttons))
        for container in tag_buttons:
            container.decompose()
        ads2 = text_tag.find_all('div',class_='google-auto-placed')
        for ad in ads2:
            ad.decompose()
        #print('number of adsbygoogle2 found: ', len(ads2))

        scripts = text_tag.find_all('script')
        #print('scripts found: ',len(scripts))
        for script in scripts:
            script.decompose()

        text_tag['class'] = 'job_description'
        job.extra_information = str(text_tag)
        print(str(text_tag))
        job_list.append(job)

    return job_list


def save_jobs_as_JSON(job_list):
    dict = {
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
                for job in job_list
            ]
    }

    # app_json = json.dumps(dict)
    # print(app_json)
    with open('example.json', 'w') as outfile:
        json.dump(dict, outfile)




if __name__ == '__main__':
    jobs = read_html_from_file()
    save_jobs_as_JSON(jobs)