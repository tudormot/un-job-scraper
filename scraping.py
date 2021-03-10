from selenium import webdriver
# import time
from utils import fuzzy_delay


from job_model import *
from bs4 import BeautifulSoup, NavigableString
import re
import logging as l
import undetected_chromedriver as uc

def read_job_from_url(url):
    l.info("Scraping following url: "+ str( url))
    job = JobModel()
    application_link, html = selenium_automation(url)

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
        l.error('cant parse office! Leaving Blank')
    if job.country is None:
        l.error('cant parse country! Leaving Blank')
    if job.city is None:
        l.error('cant parse city! Leaving Blank')
    if job.organisation is None:
        l.error('cant parse organisation! Leaving Blank')
    if job.grade is None:
        l.error('cant parse grade! Leaving Blank')


def _get_text_content(soup, job):
    text_tag = soup.find("div", class_='t' + job.id)
    if text_tag is not None:
        # we are in the normal job format
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
        remove_last_line_gibberish_and_urls(text_tag,soup)
        job.extra_information = str(text_tag)
    else:
        #we are probably in pdf job mode. let's assert this assumtion:
        l.warning("Could not scrape main text content. Possibly pdf content. Leaving blank")
        job.extra_information = None
        #TODO: the problem with pdf content is that it is not rendered by headless chrome OR firefox
        #headless chrome downloads the pdf automatially , so could in theory use this pdf for parsing
        #alternatively, could change to a non-headless browser just for when this usecase is detecte. Todo though

        # anchor_tag = soup.find('textarea')
        # if anchor_tag is None:
        #     l.critical("In _get_text_content. format of job is not recognised")
        #     job.extra_information = None
        #     return
        # else:
        #     #get the tag containig all text:
        #     text_tag = anchor_tag.parent.children[1].children[0]
        #     #delete weird class info
        #     for child in text_tag.descendants:
        #         del child['class']
        #     job.extra_information = str(text_tag)






def _decide_job_category(job):
    title = job.title
    text = job.extra_information
    pattern_internship = 'internship|intern[^a-z]'
    pattern_contractor = 'contractor|contract|consultancy|consultant'
    pattern_part_time = 'part time'

    #first try to decide based on title:
    c = len(re.findall(pattern_internship, title, re.IGNORECASE))
    if c>0:
        job.job_type = 'Internship'
        return

    #exit here in case we could not extract main text body:
    if text is None:
        job.job_type = 'Full Time '
        return

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
        chunks = closing_date_pretty.split()
        if len(chunks[3]) == 1: chunks[3] = '0' + chunks[3] # so date is dd.mm.YYYY
        return chunks[3] + '.' + my_hash[chunks[4]] + '.' + chunks[5]
    except AttributeError as e:
        # FAKE_DATE = "1.01.2025"
        l.error("Unable to find closing date for job. Leaving Blank")
        return None

def remove_last_line_gibberish_and_urls(tag,soup):
    re_pattern = r'[^ ]*(?:http://|www.|https://)[a-zA-Z0-9_/.]+'
    # print(list(tag.strings))
    no_changes_made = True
    while no_changes_made:
        for i,string in enumerate(tag.strings):
            python_string = str(string)
            found_links = re.findall(re_pattern, python_string, re.IGNORECASE)
            if found_links:
                no_changes_made = False
                link = found_links[0]
                chunks = python_string.split(link,1) # 2nd param ensures splits only in 2
                new_tag = soup.new_tag("a", href=link)
                new_tag.string= '(link)'
                str1 = NavigableString(chunks[0])
                string.replace_with(str1)
                str1.insert_after(new_tag)
                new_tag.insert_after(NavigableString(chunks[1]))
                break
        if no_changes_made:
            break
        else:
            no_changes_made = True

    l = list(tag.strings)
    l[-1].extract() #this is a gibberish code that should be removed


def get_html_from_url(url):
    USE_FIREFOX = True
    if USE_FIREFOX:
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver import DesiredCapabilities
        import os
        options = Options()
        profile = webdriver.FirefoxProfile()

        PROXY_HOST = "12.12.12.123"
        PROXY_PORT = "1234"
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", PROXY_HOST)
        profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        options.headless = True
        driver = webdriver.Firefox(options=options,executable_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'geckodriver'),firefox_profile=profile, desired_capabilities=desired)
        driver.get(url)
    else:
        options = webdriver.ChromeOptions()
        # following 2 options allow chromium to be ran as administrator
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome('/snap/bin/chromium.chromedriver', options=options)
        driver.execute_script('window.open(\''+url+'\')')
        driver.get(url)


    fuzzy_delay(1)
    html = driver.page_source
    retry = 0
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.title.string)
    # print(type(soup.title))
    if soup.title.string == "Just a moment...":
        is_cloudflare = True
    else:
        is_cloudflare = False

    while is_cloudflare and retry<4:
        retry +=1
        l.warning("detected cloudflare.")
        fuzzy_delay(8)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if soup.title.string == "Just a moment...":
            is_cloudflare = True
            l.warning("Retrying...")
        else:
            is_cloudflare = False
    if retry ==4 :
        raise Exception("could not scrape,maximum retries reached.. Maybe cloudflare protection got better? " + str(url))


    # print(html)
    return html, driver


def selenium_automation(url):
    html, driver = get_html_from_url(url)
    # get original job link:
    button = driver.find_element_by_id("more-info-button")
    button.click()
    fuzzy_delay(1)
    original_job_link = driver.current_url
    driver.close()
    driver.quit()
    return original_job_link, html