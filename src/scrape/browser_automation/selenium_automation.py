from selenium.common.exceptions import NoSuchElementException

from src.scrape.browser_automation.automation_interface import \
    AutomationInterface, UnableToParseJobException
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import logging as log
import multiprocessing as mp
import time
import numpy as np


class _SeleniumAutomation(AutomationInterface):
    def __init__(self):
        self.web_driver = uc.Chrome()
        # self.web_driver.set_page_load_timeout(20)
        # self.web_driver.set_script_timeout(20)

    def get_html_from_url(self, url: str,
                          drop_consent_button: bool = True) -> str:
        self.web_driver.get(url)
        self._fuzzy_delay(1)
        html = self.web_driver.page_source
        retry = 0
        soup = BeautifulSoup(html, 'html.parser')
        cloudflare_title_strings = [
            "Access denied | unjobs.org used Cloudflare to restrict access",
            "Just a moment..."]
        if soup.title.string in cloudflare_title_strings:
            is_cloudflare = True
        else:
            is_cloudflare = False

        while is_cloudflare and retry < 5:
            retry += 1
            log.warning("detected cloudflare.")
            self._fuzzy_delay(3)
            html = self.web_driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            if soup.title.string in cloudflare_title_strings:
                is_cloudflare = True
                log.warning("Still detected cloudflare...")
            else:
                is_cloudflare = False
        if retry == 4:
            raise Exception(
                "could not scrape,maximum retries reached in wait for "
                "cloudflare.. Maybe cloudflare protection got better? " + str(
                    url))

        if drop_consent_button:
            self._check_for_cookie_consent_button_and_clear()
        html = self.web_driver.page_source
        return html

    def _check_for_cookie_consent_button_and_clear(self):
        try:
            cookie_consent_button = self.web_driver.find_element_by_class_name(
                "css-47sehv")
            log.info("Consenting to cookies!")
            cookie_consent_button.click()
            self._fuzzy_delay(1)
        except NoSuchElementException as e:
            pass

    def get_url_after_button_press(self, initial_url,
                                   button_id='more-info-button') -> str:
        assert initial_url == self.web_driver.current_url, "this state of " \
                                                           "the browser is " \
                                                           "not what the " \
                                                           "code was " \
                                                           "expecting.."
        un_jobs_url = self.web_driver.current_url
        link = "https://unjobs.org/job_detail"
        MAX_NR_RETRIES = 5
        retry = 0
        while link == "https://unjobs.org/job_detail" and retry < \
                MAX_NR_RETRIES:
            # process = mp.Process(target=self.web_driver.execute_script(
            #     "document.getElementById('more-info-button').click()"))
            process = mp.Process(target=self.web_driver.find_element_by_id(
                'more-info-button').click, args=())
            self._fuzzy_delay(0.2)
            process.start()
            process.join(timeout=10)
            if process.exitcode is None:
                print("process has not terminated!")
                process.kill()
                if self.web_driver is not None:
                    self.web_driver.quit()
                self.web_driver = uc.Chrome()
                self.web_driver.get(un_jobs_url)
                self._check_for_cookie_consent_button_and_clear()
            else:
                link = self.web_driver.current_url

            if link == "https://unjobs.org/job_detail":
                print("Landed on https://unjobs.org/job_detail.. retrying: "
                      "", retry)
                self.web_driver.get(un_jobs_url)
                self._fuzzy_delay(0.2)
            retry += 1
        if retry == MAX_NR_RETRIES:
            #could not get the damned link, so giving up on parsing this job
            raise UnableToParseJobException("We could not get the original "
                                            "job application link")
        return link

    @staticmethod
    def _fuzzy_delay(s):
        # waits for a fuzzy amount of time. +-10% of specified time
        tol = s / 10.
        fuzz = np.random.uniform(low=-tol, high=tol)
        delay = s + fuzz
        time.sleep(delay)



# poor man's singleton
selenium_automation = _SeleniumAutomation()
