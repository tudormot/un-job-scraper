from bs4 import BeautifulSoup
import logging as log

from selenium.common.exceptions import NoSuchElementException

from src.utils import fuzzy_delay


def get_html_from_url(url, web_driver):
    web_driver.get(url)
    fuzzy_delay(1)
    html = web_driver.page_source
    retry = 0
    soup = BeautifulSoup(html, 'html.parser')
    cloudflare_title_strings = [
        "Access denied | unjobs.org used Cloudflare to restrict access",
        "Just a moment..."]
    if soup.title.string in cloudflare_title_strings:
        is_cloudflare = True
    else:
        is_cloudflare = False

    while is_cloudflare and retry < 4:
        retry += 1
        log.warning("detected cloudflare.")
        fuzzy_delay(8)
        html = web_driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if soup.title.string in cloudflare_title_strings:
            is_cloudflare = True
            log.warning("Retrying...")
        else:
            is_cloudflare = False
    if retry == 4:
        raise Exception(
            "could not scrape,maximum retries reached.. Maybe cloudflare protection got better? " + str(
                url))

    check_for_cookie_consent_button_and_clear(web_driver)
    html = web_driver.page_source
    return html


def check_for_cookie_consent_button_and_clear(web_driver):
    try:
        cookie_consent_button = web_driver.find_element_by_class_name(
            "css-47sehv")
        log.info("Seems like we have found a cookie consent button! "
                 "Trying to consent now")
        cookie_consent_button.click()
        fuzzy_delay(1)
    except NoSuchElementException as e:
        pass

