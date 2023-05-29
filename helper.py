import time
from typing import Any, Callable, List
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 10:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception("problem waiting")

class wait_for_page_load(object):
    browser: uc.Chrome
    def __init__(self, browser):
        self.browser = browser
    def __enter__(self):
        self.old_page = self.browser.find_element(By.TAG_NAME, 'html')
    def page_has_loaded(self):
        new_page = self.browser.find_element(By.TAG_NAME, 'html')
        return new_page.id != self.old_page.id
    def __exit__(self, *_):
        wait_for(self.page_has_loaded)


from multiprocessing import Pool as ThreadPool

def multiprocess(functions: List[Callable], args: List[Any], thread_num: int=4):
    pool = ThreadPool(thread_num)
    results = pool.map(functions, args)
    pool.close()
    pool.join()
    return results