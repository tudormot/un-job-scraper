from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.scrape.browser_automation.automation_interface import \
    AutomationInterface, UnableToParseJobException
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import logging as log
import multiprocessing as mp
import time
import numpy as np

from src.scrape.browser_automation.selenium.button_clicker_process import \
    ButtonClickerProcess
from src.scrape.browser_automation.selenium.common import \
    check_for_cookie_consent_button_and_clear, fuzzy_delay


class _SeleniumAutomation(AutomationInterface):
    def __init__(self):
        self.web_driver = uc.Chrome()
        # self.web_driver.set_page_load_timeout(20)
        # self.web_driver.set_script_timeout(20)

    def get_html_from_url(self, url: str,
                          drop_consent_button: bool = True) -> str:

        # print
        # try:
        #
        #     if soup.head.title.string in cloudflare_title_strings:
        #         is_cloudflare = True
        #     else:
        #         is_cloudflare = False
        # except Exception as e:

        self.web_driver.get(url)
        fuzzy_delay(1)

        cloudflare_title_strings = [
            "Access denied | unjobs.org used Cloudflare to restrict access",
            "Just a moment..."]
        retry = 0
        MAX_RETRIES_CLOUDFLARE_CHECK = 5
        while True:
            html = self.web_driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            try:
                if soup.head.title.string in cloudflare_title_strings:
                    if retry == 0:
                        log.warning("detected cloudflare.")
                    else:
                        log.warning("Still detected cloudflare...")
                    is_cloudflare = True
                    fuzzy_delay(3)
                else:
                    is_cloudflare = False
            except Exception as e:
                #todo: remove this try/except if error never gets thrown, this is
                # for debugging purposes. I got a soup.title.string = None
                # exception once, now i modified it to
                print("unexpected exception in checking for cloudflare: ",e)
                print("soup.head.title.string: ", soup.head.title.string)
                print("url = ", url)
                print('html = \n', soup.prettify())
                raise e

            if not is_cloudflare:
                break

            if retry == MAX_RETRIES_CLOUDFLARE_CHECK:
                raise Exception(
                    "could not scrape,maximum retries reached in wait for "
                    "cloudflare.. Maybe cloudflare protection got better? "
                    + str(url))
            retry += 1

        if drop_consent_button:
            check_for_cookie_consent_button_and_clear(self.web_driver)
        html = self.web_driver.page_source
        return html

    def get_url_after_button_press(self, initial_url,
                                   button_id='more-info-button') -> str:
        if initial_url != self.web_driver.current_url:
            log.warning("warning, during normal scraping workflow selenium "
                        "should be at " +
                        initial_url + " but now it is instead "
                                      "at " + self.web_driver.current_url)
            self.web_driver.get(initial_url)
            check_for_cookie_consent_button_and_clear(self.web_driver)

        un_jobs_url = self.web_driver.current_url

        link = "https://unjobs.org/job_detail"
        MAX_NR_RETRIES = 5
        retry = 0
        while link == "https://unjobs.org/job_detail" and retry < \
                MAX_NR_RETRIES:
            try:
                process = ButtonClickerProcess(args=(self.web_driver,un_jobs_url))
                fuzzy_delay(0.2)
                process.start()
                process.join(timeout=10)
            except Exception as e:
                print("no idea what we caught from spawned process: ", e)
                raise e

            if process.exitcode is None:
                print("process has not terminated!")
                process.kill()
                if self.web_driver is not None:
                    self.web_driver.quit()
                self.web_driver = uc.Chrome()
                self.web_driver.get(un_jobs_url)
                check_for_cookie_consent_button_and_clear(self.web_driver)
            else:
                link = self.web_driver.current_url

            if link == "https://unjobs.org/job_detail":
                print("Landed on https://unjobs.org/job_detail.. retrying: "
                      "", retry)
                self.web_driver.get(un_jobs_url)
                fuzzy_delay(0.2)
            retry += 1
        if retry == MAX_NR_RETRIES:
            # could not get the damned link, so giving up on parsing this job
            raise UnableToParseJobException("We could not get the original "
                                            "job application link")
        return link



    def terminate(self):
        self.web_driver.quit()


# poor man's singleton
selenium_automation = _SeleniumAutomation()
