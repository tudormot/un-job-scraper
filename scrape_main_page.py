from utils import fuzzy_delay
from bs4 import BeautifulSoup
import logging as l
import datetime

from scraping import get_html_from_url

MAGIC_URL = 'https://unjobs.org/new/'



def get_jobs_since_date(date):
    url_list = []
    page_nr = 1
    last_update_date = _get_last_update_time()
    break_loop = False

    while True:
        job_url_list, job_dates = get_urls_and_update_times_from_page(MAGIC_URL + str(page_nr))
        for i, update_date in enumerate(job_dates):
            if(update_date > date):
                url_list.append( job_url_list[i])
            else:
                break_loop = True
                break
        if break_loop:
            break

        if not job_url_list:
            l.critical('Did not find any more pages at url: '+ str( MAGIC_URL+str(page_nr)))
            l.critical('WARNING! This should really not happen!')
            break
        # url_list.extend(job_url_list)
        page_nr += 1

    return url_list, last_update_date

def get_all_job_urls():

    url_list = []
    page_nr = 1


    last_update_date = _get_last_update_time()
    while True:
        job_url_list = get_urls_from_page(MAGIC_URL + str(page_nr))
        if not job_url_list:
            l.info('Did not find any more pages at url: '+str( MAGIC_URL)+str(page_nr))
            break
        url_list.extend(job_url_list)
        page_nr += 1

    return url_list, last_update_date




def get_urls_from_page(page_url):
    fuzzy_delay(1)
    html, _= get_html_from_url(page_url)
    fuzzy_delay(1)
    soup = BeautifulSoup(html, 'html.parser')

    job_url_list = [x['href'] for x in soup.find_all("a", class_="jtitle")]

    return job_url_list

def get_urls_and_update_times_from_page(page_url):
    html, _  = get_html_from_url(page_url)
    fuzzy_delay(1)
    l.info("INFO. request to : "+ str(page_url))
    soup = BeautifulSoup(html, 'html.parser')
    job_url_list = [x['href'] for x in soup.find_all("a", class_="jtitle")]
    date_list = [string_to_datetime(x['datetime']) for x in soup.find_all('time', class_='upd timeago')]

    return job_url_list, date_list

def _get_last_update_time():
    html,_  = get_html_from_url("https://unjobs.org/")
    fuzzy_delay(1)
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('time', class_='upd timeago')
    last_update_date = string_to_datetime(tag['datetime'])
    l.info("INFO: last_update_date: "+ str( last_update_date))
    return last_update_date


def string_to_datetime(s):
    return datetime.datetime(year=int(s[0:4]), month=int(s[5:7]), day=int(s[8:10]), hour=int(s[11:13]), minute=int(s[14:16]), second=int(s[17:19]))