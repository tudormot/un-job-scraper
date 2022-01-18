import numpy as np
import time
import logging as log

from selenium.common.exceptions import TimeoutException
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
    try:
        cookie_consent_button = WebDriverWait(web_driver,
                                              2).until(
            EC.presence_of_element_located((By.CLASS_NAME,
                                            "css-47sehv"))
        )
        log.info("Consenting to cookies!")
        cookie_consent_button.click()
        fuzzy_delay(0.2)
    except TimeoutException as e:
        # not found cookie consent, no biggie
        pass