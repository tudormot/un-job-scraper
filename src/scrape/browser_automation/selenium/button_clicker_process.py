import multiprocessing as mp
import time

from selenium.common.exceptions import TimeoutException, \
    ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import logging as log

from src.scrape.browser_automation.selenium.common import \
    check_for_cookie_consent_button_and_clear

MAX_NR_BUTTON_CLICK_REATTEMPTS = 5


class ButtonClickerProcess(mp.Process):
    def __init__(self, args: tuple):
        super(ButtonClickerProcess, self).__init__(
            target=self._attempt_button_click, args=args)

    def _attempt_button_click(self, web_driver, un_jobs_url, reattempt_nr=0):
        button = None
        if reattempt_nr > MAX_NR_BUTTON_CLICK_REATTEMPTS:
            raise TooManyButtonClickAttemptsException("tried to click the "
                                                      "more info button too "
                                                      "many times, "
                                                      "something was always wrong")
        try:
            button = WebDriverWait(web_driver, 10).until(
                EC.element_to_be_clickable((By.ID, "more-info-button"))
            )
        except TimeoutException as e:
            log.error("The more-info-button is not clickable: " +
                      un_jobs_url + ". Failed parsing this job")
            raise e
        try:
            click_through_to_new_page(button)
        except ElementClickInterceptedException as e:
            log.warning("No idea why we could not click button as we "
                        "waited for it to become clickable.. alas, "
                        "this sometimes happens, "
                        "checking for cookie consent and retrying")
            if 'qc-cmp2-consent-info' in e.msg:
                check_for_cookie_consent_button_and_clear(web_driver)
                self._attempt_button_click(web_driver, un_jobs_url,
                                           reattempt_nr=reattempt_nr + 1)
            elif 'data-google-container-id' in e.msg:
                # i suspect this is due to google ads? rerun function
                self._attempt_button_click(web_driver, un_jobs_url,
                                           reattempt_nr=reattempt_nr + 1)
            else:
                # we don't even know what obstructed the button.. alas lets
                # retry
                self._attempt_button_click(web_driver, un_jobs_url,
                                           reattempt_nr=reattempt_nr + 1)


def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )


def click_through_to_new_page(button):
    button.click()

    def link_has_gone_stale():
        try:
            # poll the link with an arbitrary call
            button.find_elements(by=By.ID, value='doesnt-matter')
            return False
        except StaleElementReferenceException:
            return True

    wait_for(link_has_gone_stale)


class TooManyButtonClickAttemptsException(Exception):
    pass
