import multiprocessing as mp

from selenium.common.exceptions import TimeoutException, \
    ElementClickInterceptedException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import logging as log

from src.scrape.browser_automation.selenium.common import \
    check_for_cookie_consent_button_and_clear


MAX_NR_BUTTON_CLICK_REATTEMPTS = 5


class ButtonClickerProcess(mp.Process):
    def __init__(self, args:tuple):
        super(ButtonClickerProcess, self).__init__(
            target=self._attempt_button_click, args=args)

    def _attempt_button_click(self,web_driver,un_jobs_url,reattempt_nr = 0):
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
            button.click()
        except ElementClickInterceptedException as e:
            log.warning("No idea why we could not click button as we "
                        "waited for it to become clickable.. alas, "
                        "this sometimes happens, "
                        "checking for cookie consent and retrying")
            if 'qc-cmp2-consent-info' in e.msg:
                check_for_cookie_consent_button_and_clear(web_driver)
                self._attempt_button_click(web_driver,un_jobs_url,
                                           reattempt_nr=reattempt_nr+1)
            elif 'data-google-container-id' in e.msg:
                # i suspect this is due to google ads? rerun function
                self._attempt_button_click(web_driver,un_jobs_url,
                                           reattempt_nr=reattempt_nr+1)
            else:
                # we don't even know what obstructed the button.. alas lets
                # retry
                self._attempt_button_click(web_driver, un_jobs_url,
                                           reattempt_nr=reattempt_nr + 1)


class TooManyButtonClickAttemptsException(Exception):
    pass
