import multiprocessing as mp

from selenium.common.exceptions import TimeoutException, \
    ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import logging as log

from src.scrape.browser_automation.selenium.common import \
    check_for_cookie_consent_button_and_clear, click_through_to_new_page, \
    ButtonNotStaleException

MAX_NR_BUTTON_CLICK_REATTEMPTS = 5


class ButtonClickerProcess(mp.Process):
    def __init__(self, args: tuple):
        super(ButtonClickerProcess, self).__init__(
            target=self._attempt_button_click, args=args)

    def _attempt_button_click(self, web_driver, un_jobs_url, reattempt_nr=0):
        button = None
        should_reattempt= False
        if reattempt_nr > MAX_NR_BUTTON_CLICK_REATTEMPTS:
            raise TooManyButtonClickAttemptsException("tried to click the "
                                                      "more info button too "
                                                      "many times, "
                                                      "something was always wrong")
        try:
            button = WebDriverWait(web_driver, 4).until(
                EC.element_to_be_clickable((By.ID, "more-info-button"))
            )
        except TimeoutException as e:
            log.error("The more-info-button is not clickable: " +
                      un_jobs_url)
            raise e
        try:
            click_through_to_new_page(button)
        except ButtonNotStaleException as e:
            print(e)
            print("Not sure exactly what causes this, but retrying")
            should_reattempt = True
        except ElementClickInterceptedException as e:
            log.warning("Clicking of button was intercepted..")
            if 'qc-cmp2-summary-buttons' in e.msg:
                check_for_cookie_consent_button_and_clear(web_driver)
                should_reattempt = True
            elif 'data-google-container-id' in e.msg:
                # i suspect this is due to google ads? rerun function
                log.warning("google ads detected. Isn't adblocker installed?"
                            " It should be")
                raise e
            else:
                # we don't even know what obstructed the button..
                raise e
        if should_reattempt:
            self._attempt_button_click(web_driver, un_jobs_url,
                                       reattempt_nr=reattempt_nr + 1)



class TooManyButtonClickAttemptsException(Exception):
    pass


