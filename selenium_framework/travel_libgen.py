# #! to execute this code -> 1. download chromedriver, 2-> change driver path 27. line, 3-> download selenium
# #! this code only works on terminal, and gets two attributes size and count

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from PyPDF2 import PdfReader
import os
import requests
import pandas as pd
import argparse

parser = argparse.ArgumentParser() # gets two variable from terminal 
parser.add_argument('--size', type=int, required=True) # one of them size
parser.add_argument('--count', type=str, required=True) # one of them count
args = parser.parse_args()

data = pd.read_csv('inputs/cropped_data.csv') # reads data from cropped dataset

# Main Selenium Settings
PATH = "C:\Program Files (x86)\chromedriver.exe"  # PATH of WebDriver
get_path = "https://libgen.is/" # website address
output_dir = 'outputs' # output directory
book_language = "English" # book language
file_address = f'outputs/pdf_urls_{args.count}.txt' # you might change file_address
unique_category_count = 5658 # comes from cropped dataset
increment = float(unique_category_count / 23)

# settings of driver service
driver_service = Service(executable_path=PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


def selenium_fun(key):
    temp_pdf_url = 'None'
    # opens driver - explorer -
    driver = webdriver.Chrome(options=options, service=driver_service)
    driver.implicitly_wait(10)

    # opens libgen website
    driver.get(get_path)
    try:
        # click search button and writex text into search text field (book name)
        search = driver.find_element("id", "searchform")
        search.send_keys(key)
        search.send_keys(Keys.RETURN)

        # gets table size of second page(shows all books about our key)
        row_count = len(driver.find_elements(By.XPATH, "/html/body/table[3]/tbody/tr"))

        if row_count == 1: # website does not have this book
            driver.quit()
            return temp_pdf_url 
        else:
            for index in range(2, row_count, 1): # for every table row, searchs correct book
                language_xpath = "/html/body/table[3]/tbody/tr[" + index.__str__() + "]/td[7]" # gets language code
                language = driver.find_element(By.XPATH, language_xpath).text 

                if book_language == language:  # probably correct book
                    # gets book id
                    book_id_xpath = "/html/body/table[3]/tbody/tr[" + index.__str__() + "]/td[1]"
                    book_id = driver.find_element(By.XPATH, book_id_xpath).text
                    # clicks book name for going to other page
                    driver.find_element(By.XPATH, '//*[@id="' + book_id + '"]').click()
                    break
            try:

                driver.find_element(By.XPATH, "/html/body/table/tbody/tr[2]/td[1]/a/img").click()  # clicking image
                driver.find_element(By.XPATH, '//*[@id="download"]/ul/li[1]/a').click()  # clicking cloud fare
                
                # gets pdf_url of book
                temp_pdf_url = driver.current_url
                driver.quit()
                return temp_pdf_url

            finally:
                driver.quit()
                return temp_pdf_url
    finally:
        driver.quit()
        return temp_pdf_url


with open(file_address, 'w') as f:
    for k in range(int(args.size - increment), args.size): 
        # assign book title and book author to search_key variable
        search_key = data.iloc[k]['book_title'] + "     " + data.iloc[k]['book_author']

        # gets category name of book
        category_name = data.iloc[k]['Category']

        # from selenium_fun gets pdf url, if pdf url cannot find returns None
        pdf_url = selenium_fun(search_key)

        # writes pdf_url into txt file
        line = f'{category_name}, {pdf_url}'
        f.write(f'{line}\n')