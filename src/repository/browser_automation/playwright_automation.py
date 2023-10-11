raise Exception("playwright automation deprecated as it gets detected by cloudflare, but idea could be useful "
                "in the future")
import time
import numpy as np
from src.scrape.browser_automation.automation_interface import \
    AutomationInterface
from playwright.sync_api import sync_playwright


class _PlaywrightAutomation(AutomationInterface):
    def get_html_from_url(self, url: str,
                          drop_consent_button: bool = True) -> str:
        with sync_playwright() as p:
            browser = p.webkit.launch()
            page = browser.new_page()
            page.goto(url)
            return page.content()

    def get_url_after_button_press(self, initial_url,
                                   button_id='more-info-button') -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(initial_url)
            if page.is_visible(".css-47sehv"):
                #click cookie consent button
                print("debug, detected cookie consent button")
                page.click(".css-47sehv",timeout=5000)

            print(page.content())

            MAX_NR_RETRIES = 10
            retry = 0
            while retry < MAX_NR_RETRIES:
                page.click('id=' + button_id,timeout=10000)
                self._fuzzy_delay(20)
                url_after_click = page.url
                print("Page url is : ", url_after_click)
                if url_after_click == "https://unjobs.org/job_detail":
                    print("debug.retrying")
                    page.goto(initial_url)
                    self._fuzzy_delay(2)

                    retry +=1
                else:
                    break
            return url_after_click

    @staticmethod
    def _fuzzy_delay(s):
        # waits for a fuzzy amount of time. +-10% of specified time
        tol = s / 10.
        fuzz = np.random.uniform(low=-tol, high=tol)
        delay = s + fuzz
        time.sleep(delay)


playwrightAutomation = _PlaywrightAutomation()
