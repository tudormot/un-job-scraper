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
    # print('DEBUG.Contents of soup:')
    # print(soup.prettify())
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
    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--headless")
    driver = webdriver.Chrome('/snap/bin/chromium.chromedriver',options=options)
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

    pattern_org = 'Organization:\n'
    pattern_country = 'Country:\n'
    pattern_city_1 = 'City:\n'
    pattern_city_2 = 'Field location:\n'
    pattern_office = 'Office:\n'
    pattern_grade = 'Grade:\n'

    job.organisation = None
    job.country = None
    job.city = None
    job.grade = None
    job.office = None

    for content in contents:
        # print('content[0] is ',content[0])
        if content[0] == pattern_org:
            job.organisation = content[1].string.strip('\n')
        elif content[0] == pattern_country:
                job.country = content[1].string.strip('\n')
        elif content[0] == pattern_city_1 or content[0] == pattern_city_2:
                job.city = content[1].string.strip('\n')
        elif content[0] == pattern_grade:
                job.grade = content[1].string.strip('\n')
        elif content[0] == pattern_office:
                job.office = content[1].string.strip('\n')

    if job.office is None:
        print('INFO cant parse office! Leaving Blank')
    if job.country is None:
        print('INFO cant parse country! Leaving Blank')
    if job.city is None:
        print('INFO cant parse city! Leaving Blank')
    if job.organisation is None:
        print('INFO cant parse organisation! Leaving Blank')
    if job.grade is None:
        print('INFO cant parse grade! Leaving Blank')


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
        job.job_type = 'Contractor'
    else:
        i = len(re.findall(pattern_internship, text, re.IGNORECASE))
        if i>3:
            job.job_type= 'Internship'
        else:
            p = len(re.findall(pattern_part_time, text, re.IGNORECASE))
            if p > 2:
                job.job_type = 'Part Time'
            else:
                job.job_type = 'Full Time '



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
