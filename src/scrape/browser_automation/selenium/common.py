import numpy as np
import time
import logging as log
from bs4 import BeautifulSoup

from selenium.common.exceptions import TimeoutException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def fuzzy_delay(s):
    # waits for a fuzzy amount of time. +-10% of specified time
    tol = s / 10.
    fuzz = np.random.uniform(low=-tol, high=tol)
    delay = s + fuzz
    time.sleep(delay)

def check_for_cookie_consent_button_and_clear(web_driver):
    #first check if the cookie consent form is there:
    soup = BeautifulSoup(web_driver.page_source, 'html.parser')
    if soup.find("h2",string="We value your privacy") is not None:
        try:
            cookie_consent_button = WebDriverWait(web_driver,
                                                  4).until(
                EC.presence_of_element_located((By.CLASS_NAME,
                                                "css-1hy2vtq"))
            )
            log.info("Consenting to cookies!")
            click_through_to_new_page(button=cookie_consent_button)
            fuzzy_delay(0.2)
        except TimeoutException as e:
            raise Exception("Could not click the accept cookies button "
                            "although we have found a cookie banner.")
    else:
        # not found cookie consent, no biggie
        pass

# def click_through_simple(button, web_driver):
#     # a simpler variant of the function waiting for the button to become
#     # stale, lets see if it works
#     button.click()
#     fuzzy_delay(2)
#     pass

def click_through_to_new_page(button):
    def button_has_gone_stale():
        try:
            # poll the link with an arbitrary call
            button.find_elements(by=By.ID, value='doesnt-matter')
            return False
        except StaleElementReferenceException:
            return True

    def wait_for(condition_function,timeout = 20):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if condition_function():
                return True
            else:
                time.sleep(0.2)
        raise ButtonNotStaleException(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    button.click()
    wait_for(button_has_gone_stale)


class ButtonNotStaleException(Exception):
    pass
