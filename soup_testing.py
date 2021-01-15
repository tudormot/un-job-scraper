from scraping import *

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

def test_read_job_from_url():
    TEST_URL = "https://unjobs.org/vacancies/1610658708861"
    job = read_job_from_url(TEST_URL)
    print(job.as_dict())

if __name__ == '__main__':
    test_read_job_from_url()