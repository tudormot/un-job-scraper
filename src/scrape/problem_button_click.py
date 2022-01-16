from multiprocessing import Queue
import undetected_chromedriver as uc

def problem_button_click(un_jobs_link:str, queue: Queue):
    web_driver = uc.Chrome()
    web_driver.get(un_jobs_link)
    web_driver.find_element_by_id('more-info-button').click()
    queue.put(web_driver.current_url)
