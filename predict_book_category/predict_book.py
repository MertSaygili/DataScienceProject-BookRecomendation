# #! to execute this code -> 1. download chromedriver, 2-> change driver path 27. line, 3-> download selenium
# #! this code only works on terminal, and gets two attributes size and count and does not execute on ipynb file


from selenium import webdriver  # for web scrapping, pip install selenium
from selenium.webdriver.common.keys import Keys  # for click event
from selenium.webdriver.common.by import By  # help development kit
from selenium.webdriver.chrome.service import Service  # selenium service
from PyPDF2 import PdfFileReader  # pdf reader, pip install pypdf2==2.0
from nltk import FreqDist  # natural language tool kit library importing for  get frequency of words
from nltk.corpus import stopwords  # importing for basic stopwords
from nltk.tokenize import word_tokenize

import pandas as pd  # reading file
import random  # for creating random number
import nltk  # natural language tool kit library
import os  # file, folder organization
import requests  # for downloading api
import csv

# settings of nltk library
nltk.download('stopwords')  # downloads stopwords
nltk.download('punkt')  # downloads punkt

# reading data, picking random 
data_frame = pd.read_csv('inputs/books.csv', on_bad_lines='skip')  # reads data
data_frame = data_frame.query("language_code == 'eng'")  # picking english books only

random_number = random.randint(1, data_frame.shape[0]) - 1  # gets random number between 0 to frame size

random_book = data_frame.iloc[random_number]  # gives info about random book

print(random_book)

# selenium code, will get pdf file and analyze keys


# Main Selenium Settings
PATH = 'C:\Program Files (x86)\chromedriver.exe'  # PATH of WebDriver
get_path = 'https://libgen.is/'  # website address
book_path = 'temp_book.pdf'
output_dir = 'outputs'  # output directory
book_language = 'English'  # book language
download_path = 'outputs/temp_pdf'
category_analysis_path = 'outputs/category_analysis_txt/'

# settings of driver service
driver_service = Service(executable_path=PATH)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, service=driver_service)
driver.implicitly_wait(20)  # waits for maximum 20 seconds to travel in website, prevent errors

nltk.download('stopwords')  # downloads stopwords
nltk.download('punkt')  # downloads punkt

stop_words = set(stopwords.words('english'))  # gets english stopwords

# for getting book
def selenium_travel(key):
    temp_pdf_url = 'none'

    # opens libgen website
    driver.get(get_path)
    try:
        # click search button and writex text into search text field (book name)
        search = driver.find_element("id", "searchform")
        search.send_keys(key)
        search.send_keys(Keys.RETURN)

        # gets table size of second page(shows all books about our key)
        row_count = len(driver.find_elements(By.XPATH, "/html/body/table[3]/tbody/tr"))

        if row_count == 1:  # website does not have this book
            return temp_pdf_url
        else:
            for index in range(2, row_count, 1):  # for every table row, searches correct book
                language_xpath = "/html/body/table[3]/tbody/tr[" + index.__str__() + "]/td[7]"
                language = driver.find_element(By.XPATH, language_xpath).text

                type_xpath = "/html/body/table[3]/tbody/tr[" + index.__str__() + "]/td[9]"
                type_val = driver.find_element(By.XPATH, type_xpath).text  # type code text

                if book_language == language and type_val == 'pdf':  # probably correct book
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
                return temp_pdf_url

            finally:
                return temp_pdf_url
    finally:
        return temp_pdf_url

# downloads pdf to compputer
def download_pdf(url):
    response = requests.get(pdf_url)  # sends request to libgen website and download pdf to our computer for key analysing

    if response.status_code == 200:  # request successfull
        file_path = os.path.join(download_path, os.path.basename(book_path))  # dowloands pdf file

        with open(file_path, 'wb') as file:
            file.write(response.content)
    else:  # request failed!
        print('Request error!')

# reads pdf file
def reading_pdf():
    # extra stop words
    extra_words = [',', '.', '-', "'", '!', '?', "'s", '”', '“', ':', "''", "’", '``', ')', '(', ';', 'like', 'one',
                   'would', 'also', 'many', 'get', 'want', "n't", 'however', 'two', 'think', 'go', 'going', 'say',
                   'make',
                   '[', ']' "'re", 'ing', 'things', 'thought', 'may', 'first', 'see', 'us', 'even', 'years', 'could',
                   'says', 'new', 'said', 'way', '...', 'back', 'another', 'times', 'day', 'york', 'p.', 'never',
                   'good',
                   'much', 'right', 'still', 'must', ']', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'et',
                   '&', '‘', 'm.', 'j.', 'r.', 's.', 'd.', '%', 'away', '--', 'came', 'e', 'well', "'re", "'ll", 'made',
                   'c.', 'a.', 'l.', 'know', 'known', 'think', 'come', 'last', 'got', 'though', 'great', 'found',
                   'went',
                   "'ve", 'something', 'look', 'find', 'looked', 'without', 'told', 'three', 'might', 'asked', 'de',
                   'w',
                   'upon', 'long', 'time', 'since', 'took', 'c.', 'a.', 'l.', "'m", 'th', 'ca', 'take', 'let', 'every',
                   'david', 'ng', 'feeling', 'ever', 'thoughts', 'better', 'always', 'give', 'stop', "\x00\x00", "'d",
                   'fi',
                   'der', '\x81', '{', '#', '=', 'h', 'r', '10/10/08', 'f', 'v', 'pm', '—', '-', 'n', 'u', 'l', 'je',
                   'c',
                   'g', 'p', 'da', 'se', 'k', 'na', 'su', 'ne', 'ći', 'što', 'b', '–', 'nije', 'bi', 'za', 'od', 'će',
                   'ona', 'bio', 'li', 'iz', 'ga', 'če', 'yes', 'no', 'ali', '<', '>', 'around', 'saw', 'soon', 'use',
                   'thou', 'whole', 'thing', 'el', 'thy', 'la', 'yet', 'page', 'different', 'next', 'previous', 'often',
                   'set', 'used', '}', 'pp', 'las', 'los', '~', 'using', 'left', '0', 'done', 'later', 'although',
                   'little',
                   'else', 'henry', 'dorian', 'really', 'pilgrim', 'harry', 'anything', '•', 'jay', 'oliver', 'ed', '�',
                   'peter', 'mu', 'po', 'tako', 'joj', 'bila', 'koji', 'oh', 'put', 'kad', 'sam', 'kako', 'othello',
                   'hugo',
                   'lear', 'shakespeare', 'jessica', 'iago', 'hannah', 'bernard', 'hcederer', 'jack', 'olga', 'orestes',
                   'lizzie', 'desdemone', 'edmund', 'regan', 'shall', 'stevens', 'algernon', 'faulkner', 'bilo', 'kao',
                   'tell', 'brett', 'upita', 'bertram', '✥', '11:51', 'am12/16/11', '1s', '12/16/11', 'probably',
                   'behind',
                   '86125_letspretend_tx_p1-324.indd', 'taran', 'simon', 'barney', 'lyra', 'jill', 'gwydion', 'felt',
                   'jane',
                   'meggie', 'clare', 's0', '/', '0of0', '820', '10/3/2009', '//c', 'outlander007', 's0an0e', 'stu',
                   '`',
                   'ana0gabaldon0', 'ralph', '\\documents0and0settings\\nickunj\\desktop\\di' 'ana0gabaldon0', '0page0',
                   'larry', 'harold', 'mike', "didnʼt", 'began', 'enough', 'tom', 'nick', 'seemed', "donʼt", 'stu',
                   '\x01',
                   'er', 'nd', 'ou', 'en', 'sa', 'ar', 'ea', 'ow', 'oo', 'e.', 'yo', '..', 'gh', 'ut', 'ho', 'ad', 'ha',
                   'ee',
                   'co', 't.', 'ot.', 'te', 'ay', 'es', 'sh', 'om', 'un', 'ba', 'pe', 'ge', 'ke', 'von', 'fo', 'bo',
                   'ot',
                   'ta', 'hi', '\xad', 'ver', 'nt', 'al', 'tr', 'n.', 'j',
                   ]
    temp_book_path = f'{download_path}/{book_path}'  # path address of pdf
    content = ''  # empty content

    for word in extra_words:  # adds extra words to stop_words list
        stop_words.add(word)

    with open(temp_book_path, 'rb') as pdf:  # opens pdf file
        pdf_read = PdfFileReader(pdf)  # for reading

        for page in pdf_read.pages:  # reads pdf page by page
            try:
                content = content + page.extractText() + '\n'
            except Exception:
                print(Exception)

    content = content.lower()  # makes all content lower case, help us to analyze pdf
    word_s = word_tokenize(content) 
    real_content = [] 

    for word in word_s:  # deletes stop words from content
        if word not in stop_words:
            real_content.append(word)

    word_dict = FreqDist(real_content)
    most_repeated_words = word_dict.most_common(100)  # gets most repeated 100 word
 
    return most_repeated_words  # returns most commont words

# compares our analyze with other categories
def compare_pdf(words):
    all_txt_files = os.listdir(category_analysis_path)  # txt files path
    category_names = []  # will hold category names
    index = int(0)
    word_counter = int(0)
    category_points = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for text in all_txt_files:  # reads all category txt files
        category_names.append(text.replace('.txt', ''))

        with open(f'{category_analysis_path}{text}', encoding='utf8') as f:  # opens txt files
            lines = f.readlines()  # gets all text inside it

            for line in lines:  # reads txt file line by line
                temp_line = line.split('-')[0]

                # compare keywords
                for word in words:
                    if word[0] == temp_line:
                        category_points[index] = category_points[index] + 1

                
    
        index = index + 1

    total_point = int(0)

    #  calculates total point for normalizing
    for i in range(0, len(category_names), 1):
        total_point = total_point + category_points[i]

    rates = []  # for save rates of categories

    if total_point != 0:
        for i in range(0, len(category_names), 1):
            temp_c = (category_points[i] / total_point) * 100  
            rates.append(temp_c)  

            create_csv(temp_c, category_names)  # creates csv file
    else:
        print('category cannot defined')


#  creates csv file
def create_csv(rates, category_names):
    fields = ['rates', 'category_names']  # fields
    csv_rows = [fields]  # rows

    for i in range(0, len(category_names), 1):
        temp_row = [rates.__getitem__(i), category_names[i]]
        csv_rows.append(temp_row)

    filename = 'predict_rate.csv'  # defines file name

    with open(filename, 'w', encoding='utf-8', newline='') as file:  # opens file and writes rows list into it
        writer = csv.writer(file)
        writer.writerows(csv_rows)


search_key = random_book['title']  # assign book name to search_key
pdf_url = selenium_travel(search_key)  # tries to get pdf_url
driver.quit()  # closes driver


if pdf_url != 'none':
    download_pdf(pdf_url)
    common_words = reading_pdf()
    compare_pdf(common_words)

else:
    print(f'Not find file, book name = {search_key}')

