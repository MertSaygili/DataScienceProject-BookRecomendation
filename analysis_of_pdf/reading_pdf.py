# To execute code, you need to identify category name, length of pdf files (9. and 11. line)

import nltk  # natural language tool kit library
from PyPDF2 import PdfFileReader  # pdf reader, #!for download it, to terminal write pip install PyPDF2
from nltk import FreqDist  # natural language tool kit library importing for  get frequency of words
from nltk.corpus import stopwords  # importing for basic stopwords
from nltk.tokenize import word_tokenize

category_name = 'Medical'  # category name, change category name and length_of_file in every time I execute code
main_path = f'pdfs/Medical/'  # main path of category folder
length_of_file = 11   # length of pdf_files, pdf count in  specific category folder

# settings of nltk library
nltk.download('stopwords')  # downloads stopwords
nltk.download('punkt')  # downloads punkt

stop_words = set(stopwords.words('english'))  # gets english stopwords

# defines extra words to add stop_words list
extra_words = [',', '.', '-', "'", '!', '?', "'s", '”', '“', ':', "''", "’", '``', ')', '(', ';', 'like', 'one',
               'would', 'also', 'many', 'get', 'want', "n't", 'however', 'two', 'think', 'go', 'going', 'say', 'make',
               '[', ']' "'re", 'ing', 'things', 'thought', 'may', 'first', 'see', 'us', 'even', 'years', 'could',
               'says', 'new', 'said', 'way', '...', 'back', 'another', 'times', 'day', 'york', 'p.', 'never', 'good',
               'much', 'right', 'still', 'must', ']', '*', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'et',
               '&', '‘', 'm.', 'j.', 'r.', 's.', 'd.', '%', 'away', '--', 'came', 'e', 'well', "'re", "'ll", 'made',
               'c.', 'a.', 'l.', 'know', 'known', 'think', 'come', 'last', 'got', 'though', 'great', 'found', 'went',
               "'ve", 'something', 'look', 'find', 'looked', 'without', 'told', 'three', 'might', 'asked', 'de', 'w',
               'upon', 'long', 'time', 'since', 'took', 'c.', 'a.', 'l.', "'m", 'th', 'ca', 'take', 'let', 'every',
               'david', 'ng', 'feeling', 'ever', 'thoughts', 'better', 'always', 'give', 'stop', "\x00\x00", "'d", 'fi',
               'der', '\x81', '{', '#', '=', 'h', 'r', '10/10/08', 'f', 'v', 'pm', '—', '-', 'n', 'u', 'l', 'je', 'c',
               'g', 'p', 'da', 'se', 'k', 'na', 'su', 'ne', 'ći', 'što', 'b', '–', 'nije', 'bi', 'za', 'od', 'će',
               'ona', 'bio', 'li', 'iz', 'ga', 'če', 'yes', 'no', 'ali', '<', '>', 'around', 'saw', 'soon', 'use',
               'thou', 'whole', 'thing', 'el', 'thy', 'la', 'yet', 'page', 'different', 'next', 'previous', 'often',
               'set', 'used', '}', 'pp', 'las', 'los', '~', 'using', 'left', '0', 'done', 'later', 'although', 'little',
               'else', 'henry', 'dorian', 'really', 'pilgrim', 'harry', 'anything', '•', 'jay', 'oliver', 'ed', '�',
               'peter', 'mu', 'po', 'tako', 'joj', 'bila', 'koji', 'oh', 'put', 'kad', 'sam', 'kako', 'othello', 'hugo',
               'lear', 'shakespeare', 'jessica', 'iago', 'hannah', 'bernard', 'hcederer', 'jack', 'olga', 'orestes',
               'lizzie', 'desdemone', 'edmund', 'regan', 'shall', 'stevens', 'algernon', 'faulkner', 'bilo', 'kao',
               'tell', 'brett', 'upita', 'bertram', '✥', '11:51', 'am12/16/11', '1s', '12/16/11', 'probably', 'behind',
               '86125_letspretend_tx_p1-324.indd', 'taran', 'simon', 'barney', 'lyra', 'jill', 'gwydion', 'felt', 'jane',
               'meggie', 'clare', 's0', '/', '0of0', '820', '10/3/2009', '//c', 'outlander007', 's0an0e', 'stu', '`',
               'ana0gabaldon0', 'ralph', '\\documents0and0settings\\nickunj\\desktop\\di' 'ana0gabaldon0', '0page0',
               'larry', 'harold', 'mike', "didnʼt", 'began', 'enough', 'tom', 'nick', 'seemed', "donʼt", 'stu', '\x01',
               'er', 'nd', 'ou', 'en', 'sa', 'ar', 'ea', 'ow', 'oo', 'e.', 'yo', '..', 'gh', 'ut', 'ho', 'ad', 'ha', 'ee',
               'co', 't.', 'ot.', 'te', 'ay', 'es', 'sh', 'om', 'un', 'ba', 'pe', 'ge', 'ke', 'von', 'fo', 'bo', 'ot',
               'ta', 'hi', '\xad', 'ver', 'nt', 'al', 'tr', 'n.', 'j',
               ]
content = ''  # keeps whole text for analysing frequency of words

# adds extra words into stop_words list
for word in extra_words:
    stop_words.add(word)

# reading all pdf's of specific category
for i in range(1, length_of_file, 1):
    print(i)
    # defines book path
    book_path_temp = f'{main_path}{i}.pdf'
    # opens pdf file
    with open(book_path_temp, 'rb') as pdf:
        # defines pdf reader function
        pdf_temp = PdfFileReader(pdf)
        # one by one gets text of every page
        for page in pdf_temp.pages:
            # adds text of pdf into to content variable
            content = content + page.extractText() + '\n'

# do all words inside of content lower  A->a
content = content.lower()

word_s = word_tokenize(content)
real_content = []

# reads word by word to content variable
for word in word_s:
    # if word is not one of the stop words, add that word to real_content
    if word not in stop_words:
        real_content.append(word)

# takes frequency of every word inside of real_content
word_dict = FreqDist(real_content)
# gets maximum repeated 25 word
most_common_words = word_dict.most_common(25)

# prints most common words (25)
print(most_common_words)

# defines path for saving most common words
write_path = f"outputs/category_analysis/{category_name}"

# creates txt file that holds most common words
with open(f'{write_path}.txt', 'w', encoding='utf-8') as file:
    # writes into txt file
    file.write('\n'.join(f'{word[0]}-{word[1]}' for word in most_common_words))
