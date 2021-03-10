import unittest
from scrape_main_page import *

class MainPageScraper(unittest.TestCase):
    def setUp(self):
        # self.widget = Widget('The widget')
        pass


    def test_0_number_of_jobs_per_page(self):
        MAGIC_URL = "https://unjobs.org/"
        job_url_list = get_urls_from_page(MAGIC_URL)
        print(job_url_list)
        self.assertEqual(len(job_url_list), 25,
                         'incorrect number of jobs found on main page')
if __name__ == '__main__':
    unittest.main()