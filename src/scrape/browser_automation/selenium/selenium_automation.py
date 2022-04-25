import atexit

from src.scrape.browser_automation.automation_interface import \
    AutomationInterface, UnableToParseJobException
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import logging as log

from src.scrape.browser_automation.selenium.button_clicker_process import \
    ButtonClickerProcess
from src.scrape.browser_automation.selenium.common import \
    check_for_cookie_consent_button_and_clear, fuzzy_delay

#also see: https://blog.adblockplus.org/development-builds/suppressing-the-first-run-page-on-chrome
ADBLOCK_EXTENSION_DIR='/home/tudor/.config/google-chrome/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/4.46.0_0'
class SeleniumAutomation(AutomationInterface):
    def _get_web_driver(self):
        options = uc.ChromeOptions()
        options.add_argument('--load-extension='+ADBLOCK_EXTENSION_DIR)

        driver = uc.Chrome(options=options)
        driver.minimize_window()
        driver.minimize_window()

        return driver

    def __init__(self):
        self.web_driver = self._get_web_driver()
        self.process = None

    def get_html_from_url(self, url: str,
                          drop_consent_button: bool = True) -> str:
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
                # todo: remove this try/except if error never gets thrown, this is
                # for debugging purposes. I got a soup.title.string = None
                # exception once, now i modified it to
                print("unexpected exception in checking for cloudflare: ", e)
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
                self.process = ButtonClickerProcess(args=(self.web_driver,
                                                          un_jobs_url))
                fuzzy_delay(0.2)
                self.process.start()
                self.process.join(timeout=10)
            except Exception as e:
                print("no idea what we caught from spawned process: ", e)
                raise e

            if self.process.exitcode is None:
                print("process has not terminated!")
                self.process.kill()
                if True:
                    if self.web_driver is not None:
                        self.web_driver.quit()
                    self.web_driver = self._get_web_driver()
                    self.web_driver.get(un_jobs_url)
                else:
                    # in cases there are problems with this new method of
                    # fixing web_automator getting stuck, use the method in
                    # the other branch of this if statement
                    self.web_driver.reconnect()
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
        # self.web_driver.close()
        self.web_driver.quit()
        #this is required as undetected chromedriver is using this atexit
        # method to kill some processes...
        atexit._run_exitfuncs()
        if self.process:
            self.process.kill()

