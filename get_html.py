from bs4 import BeautifulSoup
import requests

r = requests.get('https://internationalcareerfinder.com/wp-json/')
#soup = BeautifulSoup(html_doc, 'html.parser')