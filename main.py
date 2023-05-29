# import os
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager


total_pages = 30

import csv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from helper import multiprocess, wait_for_page_load

driver = uc.Chrome()

def get_property_rows(url):
    township_row_class = "TransactionTablestyle__Tr-bkFlmP"
    property_transaction_table_class = "TransactionTablestyle__Table-jtHFaH"
    property_rows = []
    headers = None
    for i in range(11):
        driver.get(url)
        township_rows = driver.find_elements(By.CLASS_NAME, township_row_class)

        if i == 0:
            continue

        township_name = township_rows[i].find_element(By.TAG_NAME, 'td').text.replace("\n", ', ')

        with wait_for_page_load(driver):
            township_rows[i].click()
        
        property_transaction_table = driver.find_element(By.CLASS_NAME, property_transaction_table_class)
        
        if not headers:
            thead = property_transaction_table.find_element(By.TAG_NAME, "thead")
            thead_row = thead.find_element(By.TAG_NAME, "tr")
            headers = ["Township Name"]+[d.text for d in thead_row.find_elements(By.TAG_NAME, 'th')]

        property_transaction_table_tbody = property_transaction_table.find_element(By.TAG_NAME, 'tbody')
        for row in property_transaction_table_tbody.find_elements(By.TAG_NAME, 'tr'):
            property_rows.append([township_name]+[d.text for d in row.find_elements(By.TAG_NAME, 'td')])
            
    return headers, property_rows


if __name__ == "__main__":
    url_to_scrape = lambda page_index: f"https://www.iproperty.com.my/transaction-price/residential/?page={page_index}"
    cumulative_property_rows = []
    for page_index in range(1, 100):
        headers, property_rows = get_property_rows(url_to_scrape(page_index))
        cumulative_property_rows.extend(property_rows)

    with open('house_transactions.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile)
        wr.writerows([headers]+cumulative_property_rows)