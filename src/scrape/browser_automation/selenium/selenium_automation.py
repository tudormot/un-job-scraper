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
# go to abp-background.js and search for "suppress_first_run_page" to close
# annoying page
ADBLOCK_EXTENSION_DIR='/home/tudor/.config/google-chrome/Default/Extensions' \
                      '/gighmmpiobklfepjocnamgkkbiglidom/4.46.1_1'
class SeleniumAutomation(AutomationInterface):
    ANNOYING_JOB_DETAIL_LINK = "https://unjobs.org/job_detail"
    def _get_web_driver(self):
        options = uc.ChromeOptions()
        options.add_argument('--load-extension='+ADBLOCK_EXTENSION_DIR)

        driver = uc.Chrome(options=options,version_main=101)
        # driver.minimize_window()
        # driver.set_window_size(1, 1)

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
            if soup.head.title.string in cloudflare_title_strings:
                if retry == 0:
                    log.warning("detected cloudflare.")
                else:
                    log.warning("Still detected cloudflare...")
                fuzzy_delay(3)
            else:
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
            # this code was added for testing purposes..
            log.warning("warning, during normal scraping workflow selenium "
                        "should be at " +
                        initial_url + " but now it is instead "
                                      "at " + self.web_driver.current_url)
            self.web_driver.get(initial_url)

        un_jobs_url = self.web_driver.current_url
        check_for_cookie_consent_button_and_clear(self.web_driver)

        MAX_NR_RETRIES = 5
        retry = 0
        while retry < \
                MAX_NR_RETRIES:
            self.process = ButtonClickerProcess(args=(self.web_driver,
                                                      un_jobs_url))

            fuzzy_delay(0.2)
            try:
                self.process.start()
                self.process.join(timeout=20)
            except Exception as e:
                log.warning("Unknown exception thrown by the button clicker "
                            "process!")
                self.process.kill()
                raise e

            if self.process.exitcode is None:
                print("Process has not terminated!")
                if self.web_driver is not None:
                    self.web_driver.quit()
                self.web_driver = self._get_web_driver()
                self.web_driver.get(un_jobs_url)
                check_for_cookie_consent_button_and_clear(self.web_driver)
                retry += 1
                continue
            else:
                print("DEBUG. Process terminated normally")

            link = self.web_driver.current_url
            if link == self.ANNOYING_JOB_DETAIL_LINK:
                fuzzy_delay(2)
                if link == self.ANNOYING_JOB_DETAIL_LINK:
                    link = self.web_driver.get(un_jobs_url)
                    log.warning("Even after witing 2 seconds, we still on "
                                "job_details page")
                    retry += 1
                    continue
                else:
                    #SUCCESS!
                    break
            else:
                # SUCCESS!
                break

        if retry == MAX_NR_RETRIES:
            # could not get the damned link, so giving up on parsing this job
            raise UnableToParseJobException("We could not get the original "
                                            "job application link")
        print("### link we got after button pressed: ", link)
        return link

    def terminate(self):
        # self.web_driver.close()
        self.web_driver.quit()
        #this is required as undetected chromedriver is using this atexit
        # method to kill some processes...
        atexit._run_exitfuncs()
        if self.process:
            self.process.kill()

