import undetected_chromedriver.v2 as uc

options = uc.ChromeOptions()
options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
options.add_argument('--headless')
web_driver = uc.Chrome(options=options)


#deprecated code, might help with setting up anticloudflare in the future
#     USE_FIREFOX = False
#     if USE_FIREFOX:
#         from selenium.webdriver.firefox.options import Options
#         from selenium.webdriver import DesiredCapabilities
#         import os
#         options = Options()
#         profile = webdriver.FirefoxProfile()
#
#         PROXY_HOST = "12.12.12.123"
#         PROXY_PORT = "1234"
#         profile.set_preference("network.proxy.type", 1)
#         profile.set_preference("network.proxy.http", PROXY_HOST)
#         profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
#         profile.set_preference("dom.webdriver.enabled", False)
#         profile.set_preference('useAutomationExtension', False)
#         profile.update_preferences()
#         desired = DesiredCapabilities.FIREFOX
#         # options.headless = True
#         driver = webdriver.Firefox(options=options,executable_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'geckodriver'),firefox_profile=profile, desired_capabilities=desired)
#         driver.get(url)
#     else:
#         options = webdriver.ChromeOptions()
#         # following 2 options allow chromium to be ran as administrator
#         # options.add_argument('--no-sandbox')
#         # options.add_argument('--disable-dev-shm-usage')
#         user_agent = "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
#         options.add_argument("user-agent=" + user_agent)
#         # options.add_argument("--start-maximized")
#         options.add_argument("--headless")
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_argument("--disable-blink-features")
#         options.add_argument("--disable-blink-features=AutomationControlled")
#         options.add_argument("--enable-javascript")
#         driver = webdriver.Chrome('/home/tudor/Downloads/Installers/chromedriver_linux64/chromedriver', options=options)
#         driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#             "source": """
#                         Object.defineProperty(navigator, 'webdriver', {
#                           get: () => undefined
#                         })
#                       """
#         })
#         # driver.execute_script('window.open(\''+url+'\')')
#         driver.get(url)

    # driver = uc.Chrome()
    # just some options passing in to skip annoying popups
