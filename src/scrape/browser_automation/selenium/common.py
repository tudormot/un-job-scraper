from functools import partial

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
    # first check if the cookie consent form is there:
    found_normal_cookie_banner = False
    found_customize_cookies_banner = False
    soup = BeautifulSoup(web_driver.page_source, 'html.parser')
    if soup.find("h2", string="We value your privacy") is not None:
        try:
            cookie_consent_button = WebDriverWait(web_driver,
                                                  4).until(
                EC.presence_of_element_located((By.CLASS_NAME,
                                                "css-1hy2vtq"))
            )
            log.info("Found standard accept cookies banner. Consenting to "
                     "cookies!")
            found_normal_cookie_banner = True
            click_through_to_new_page(button=cookie_consent_button)
            fuzzy_delay(0.2)
        except TimeoutException as e:
            # no biggie, did not find normal_cookie_banner
            pass
        try:
            cookie_consent_button = WebDriverWait(web_driver,
                                                  4).until(
                EC.presence_of_element_located((By.CLASS_NAME,
                                                "css-47sehv"))
            )
            # WebDriverWait(web_driver,4).until(
            #     EC.element_to_be_clickable(cookie_consent_button)
            # )
            log.info("Found customize cookies banner. Consenting to "
                     "cookies!")
            found_customize_cookies_banner = True
            click_through_to_new_page(button=cookie_consent_button,
                                      alternative_clicking_fun=
                                      partial(click_via_javascript,
                                              web_driver,
                                              "document.getElementsByClassName("
                                              "'css-47sehv')["
                                              "0].click()"))
            fuzzy_delay(0.2)
        except TimeoutException as e:
            # no biggie, did not find customize cookies banner
            pass

        if not found_normal_cookie_banner and not \
                found_customize_cookies_banner:
            raise Exception("Problem, we encountered some sort of cookie "
                            "banner, but could not find the buttons to "
                            "minimise the banners")
    else:
        # not found cookie related annoying banners, no biggie
        pass


def click_through_to_new_page(button, alternative_clicking_fun=None):
    def button_has_gone_stale():
        try:
            # poll the link with an arbitrary call
            button.find_elements(by=By.ID, value='doesnt-matter')
            return False
        except StaleElementReferenceException:
            return True

    def wait_for(condition_function, timeout=20):
        start_time = time.time()
        while time.time() < start_time + timeout:
            if condition_function():
                return True
            else:
                print("debug,sleeping 0.2")
                time.sleep(0.2)
        raise ButtonNotStaleException(
            'Timeout waiting for {}'.format(condition_function.__name__)
        )

    if not alternative_clicking_fun:
        button.click()
    else:
        alternative_clicking_fun()
    wait_for(button_has_gone_stale)


def click_via_javascript(web_driver, javascript_string):
    # actionChains = ActionChains(web_driver)
    # actionChains.move_to_element(element).click().perform()

    web_driver.execute_script(javascript_string)


class ButtonNotStaleException(Exception):
    pass
