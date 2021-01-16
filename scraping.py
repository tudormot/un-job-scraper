from selenium import webdriver
import time
from job_model import *
from bs4 import BeautifulSoup
import re


def read_job_from_url(url):
    print("Scraping following url: ", url)
    job = JobModel()
    application_link, html = _selenium_automation(url)
    job.original_job_link = application_link
    soup = BeautifulSoup(html, 'html.parser')

    # get ID and title
    id = url.split('/')[-1]
    job.id = id
    job.title = soup.h2.string
    assert job.title is not None, 'ERROR parsing job title! in url ' + url

    _get_info_from_contents_container(soup, job)

    # get closing date
    tag = soup.find("div", class_='job' + job.id)
    iter = tag.children
    _ = iter.__next__()
    t = iter.__next__()
    job.closing_date_pretty = t.string
    job.closing_date = _parse_string_for_date(job.closing_date_pretty)

    # get tags
    job.tags = [x.a.string for x in soup.find_all("div", class_="md-chip md-chip-raised md-chip-hover")[1:]]

    _get_text_content(soup, job)
    _decide_job_category(job)

    return job


def _selenium_automation(url):
    driver = webdriver.Chrome('/snap/bin/chromium.chromedriver')
    driver.get(url)
    html = driver.page_source

    # get original job link:
    button = driver.find_element_by_id("more-info-button")
    button.click()
    time.sleep(2)
    original_job_link = driver.current_url
    return original_job_link, html


def _get_info_from_contents_container(soup, job):
    contents = [x.contents for x in soup.find_all("li", class_="list-group-item dropdown-toggle")]
    contents.pop()  # drop twitter button information

    assert contents[0][0] == 'Organization:\n', 'ERROR parsing organization posting the job!'
    job.organisation = contents[0][1].string.strip('\n')
    assert contents[1][0] == 'Country:\n', 'ERROR parsing country of job!'
    job.country = contents[1][1].string.strip('\n')
    assert contents[2][0] == 'City:\n' or contents[2][0] == 'Field location:\n', 'ERROR parsing city of  job!'
    job.city = contents[2][1].string.strip('\n')
    assert contents[3][0] == 'Office:\n', 'ERROR parsing office of job!'
    job.office = contents[3][1].string.strip('\n')
    try:
        assert contents[4][0] == 'Grade:\n', 'ERROR parsing grade of job!'
        job.grade = contents[4][1].string.strip('\n')
    except:
        job.grade = None


def _get_text_content(soup, job):
    text_tag = soup.find("div", class_='t' + job.id)
    ads = text_tag.find_all('ins', class_='adsbygoogle')
    for ad in ads:
        ad.decompose()
    tag_buttons = text_tag.find_all("div", class_='md-chips')
    for container in tag_buttons:
        container.decompose()
    ads2 = text_tag.find_all('div', class_='google-auto-placed')
    for ad in ads2:
        ad.decompose()
    scripts = text_tag.find_all('script')
    for script in scripts:
        script.decompose()

    text_tag['class'] = 'job_description'
    job.extra_information = str(text_tag)

def _decide_job_category(job):
    text = job.extra_information
    pattern_internship = 'internship|intern[^a-z]'
    pattern_contractor = 'contractor|contract|consultancy|consultant'
    pattern_part_time = 'part time'


    c = len(re.findall(pattern_contractor, text, re.IGNORECASE))
    if c>2:
        job.job_category = 'Contractor'
    else:
        i = len(re.findall(pattern_internship, text, re.IGNORECASE))
        if i>3:
            job.job_category = 'Internship'
        else:
            p = len(re.findall(pattern_part_time, text, re.IGNORECASE))
            if p > 2:
                job.job_category = 'Part Time'
            else:
                job.job_category = 'Full Time '


# def read_jobs_from_file():
#     raise Exception('deprecated')
#     offline_jobs_dir= "offline_jobs"
#     job_list = []
#     for file in os.listdir(offline_jobs_dir)[:4]: #TODO limit to 1 is temp
#
#         uri = pathlib.Path(os.path.abspath(offline_jobs_dir + '/' + file)).as_uri()
#
#         driver = webdriver.Chrome('/snap/bin/chromium.chromedriver')
#         driver.get(uri)
#
#         html = driver.page_source
#         id = file.split('.')[0]
#
#         soup = BeautifulSoup(html, 'html.parser')
#         job = JobModel()
#         job.id = id
#         job.title = soup.h2.string
#         if job.title == None:
#             print('ERROR parsing job title! TODO add in what link')
#
#         contents = [x.contents for x in soup.find_all("li", class_="list-group-item dropdown-toggle")]
#         contents.pop()  # drop twitter button information
#
#         assert contents[0][0] == 'Organization:\n', 'ERROR parsing organization posting the job!'
#         job.organisation = contents[0][1].string.strip('\n')
#         assert contents[1][0] == 'Country:\n', 'ERROR parsing country of job!'
#         job.country = contents[1][1].string.strip('\n')
#         assert contents[2][0] == 'City:\n', 'ERROR parsing city of  job!'
#         job.city = contents[2][1].string.strip('\n')
#         assert contents[3][0] == 'Office:\n', 'ERROR parsing office of job!'
#         job.office = contents[3][1].string.strip('\n')
#         try:
#             assert contents[4][0] == 'Grade:\n', 'ERROR parsing grade of job!'
#             job.grade = contents[4][1].string.strip('\n')
#         except:
#             job.grade = None
#
#         # get closing date
#         tag = soup.find("div", class_='job' + job.id)
#         iter = tag.children
#         _ = iter.__next__()
#         t = iter.__next__()
#         job.closing_date_pretty = t.string
#         job.closing_date = _parse_string_for_date(job.closing_date_pretty)
#         #print(job.closing_date)
#
#         # get tags
#         job.tags = [x.a.string for x in soup.find_all("div", class_="md-chip md-chip-raised md-chip-hover")[1:]]
#         #print(job.tags)
#
#         #get original job link: TODO: button needs to be pressed twice only when using html from file take that into account
#         button = driver.find_element_by_id("more-info-button")
#         time.sleep(2)  # 2s
#         button.click()
#         time.sleep(2) #2s
#         button = driver.find_element_by_id("more-info-button")
#         button.click()
#         time.sleep(2)
#         job.original_job_link = driver.current_url
#         #print('debug, original linK: ', job.original_job_link)
#
#         #get text content
#         text_tag= soup.find("div", class_='t' + job.id)
#         #print('text_tag is', text_tag)
#
#         # bmore = text_tag.find('div',class_='bmore')
#         # bmore.decompose()
#
#         ads = text_tag.find_all('ins', class_='adsbygoogle')
#         #print('number of adsbygoogle found: ', len(ads))
#         for ad in ads:
#             ad.decompose()
#         tag_buttons = text_tag.find_all("div",class_ = 'md-chips')
#         #print('number of tag containers found: ', len(tag_buttons))
#         for container in tag_buttons:
#             container.decompose()
#         ads2 = text_tag.find_all('div',class_='google-auto-placed')
#         for ad in ads2:
#             ad.decompose()
#         #print('number of adsbygoogle2 found: ', len(ads2))
#
#         scripts = text_tag.find_all('script')
#         #print('scripts found: ',len(scripts))
#         for script in scripts:
#             script.decompose()
#
#         text_tag['class'] = 'job_description'
#         job.extra_information = str(text_tag)
#         print(str(text_tag))
#         job_list.append(job)
#
#     return job_list
#
# def job_from_html(html,id):
#     raise Exception('deprecated')
#     soup = BeautifulSoup(html, 'html.parser')
#     job = JobModel()
#     job.id = id
#     job.title = soup.h2.string
#     if job.title == None:
#         print('ERROR parsing job title! TODO add in what link')
#
#     contents = [x.contents for x in soup.find_all("li", class_="list-group-item dropdown-toggle")]
#     contents.pop()  # drop twitter button information
#
#     assert contents[0][0] == 'Organization:\n', 'ERROR parsing organization posting the job!'
#     job.organisation = contents[0][1].string.strip('\n')
#     assert contents[1][0] == 'Country:\n', 'ERROR parsing country of job!'
#     job.country = contents[1][1].string.strip('\n')
#     assert contents[2][0] == 'City:\n', 'ERROR parsing city of  job!'
#     job.city = contents[2][1].string.strip('\n')
#     assert contents[3][0] == 'Office:\n', 'ERROR parsing office of job!'
#     job.office = contents[3][1].string.strip('\n')
#
#     #get closing date
#     tag = soup.find("div", class_='job'+job.id)
#     iter = tag.children
#     _ = iter.__next__()
#     t = iter.__next__()
#     job.closing_date_pretty = t.string
#     job.closing_date = _parse_string_for_date(job.closing_date_pretty)
#     print(job.closing_date)
#
#     #get tags
#     job.tags = [x.a.string for x in soup.find_all("div", class_="md-chip md-chip-raised md-chip-hover")[1:]]
#     print(job.tags)
#
#     return job


def _parse_string_for_date(closing_date_pretty):
    my_hash = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }
    try:
        list = closing_date_pretty.split()
        return list[3] + '.' + my_hash[list[4]] + '.' + list[5]
    except AttributeError as e:
        FAKE_DATE = "1.01.2025"
        print("Unable to find closing date for job. Setting closing date to: " + FAKE_DATE)
        return FAKE_DATE
