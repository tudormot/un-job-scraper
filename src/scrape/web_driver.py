import undetected_chromedriver as uc
import selenium.webdriver.remote.webdriver as sel

web_driver = uc.Chrome(use_subprocess=True)
web_driver.set_page_load_timeout(20)
web_driver.set_script_timeout(20)

