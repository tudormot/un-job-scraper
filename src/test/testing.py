import unittest

from src.scrape.browser_automation.playwright_automation import \
    _PlaywrightAutomation


class MainPageScraper(unittest.TestCase):
    def setUp(self):
        # self.widget = Widget('The widget')
        pass

    # def test_0_number_of_jobs_per_page(self):
    #     MAGIC_URL = "https://unjobs.org/"
    #     job_url_list = _PlaywrightAutomation().get_html_from_url(MAGIC_URL)


    def test_1_get_original_job_link(self):
        MAGIC_URL = "https://unjobs.org/vacancies/1642076044496"
        _PlaywrightAutomation().get_url_after_button_press(MAGIC_URL)





if __name__ == '__main__':
    unittest.main()
