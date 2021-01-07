from bs4 import BeautifulSoup
import requests
from config import args
from fake_useragent import UserAgent
import logging as l


ua = UserAgent()
header = {'User-Agent':str(ua.chrome)}
r = requests.get(args['root_url'],headers= header)
soup = BeautifulSoup(r.text, 'html.parser')

job_url_list = [x['href'] for x in soup.find_all("a", class_="jtitle")]

for url in job_url_list[:5]:
    filename = url.split('/')[-1]
    l.info('saving html is file: ', filename,'.html')
    job_html = requests.get(url, headers=header)
    with open('offline_jobs/' + filename + '.html', 'w') as file:
        file.write(job_html.text)


#print(soup.prettify())