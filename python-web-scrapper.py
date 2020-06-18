import requests
import sys
from bs4 import BeautifulSoup

URL = "https://www.scimagojr.com/journalsearch.php?q=4700151918&tip=sid&clean=0"

def getJournalInfo(soup):
    journal_name = soup.find_all('h1')[0].get_text().replace('\n', '').lstrip()
    home_page_tag = soup.find_all('a', id="question_journal")[0]['href']
    h_index_tag = soup.find_all('div', class_="hindexnumber")[0].get_text()
    return (journal_name, h_index_tag, home_page_tag)


def getPageContent(URL):
    html = requests.get(URL)
    success = False if html.status_code != 200 else True
    soup = BeautifulSoup(html.content, 'html.parser')
    return (success, soup)

def getAllURLS(urls_file):
    content = []
    with open(urls_file) as f:
        lines = f.readlines()
        content = [line.rstrip() for line in lines]
    return content

def sortFunction(t):
    return int(t[1])


# Check if everything is correct
if len(sys.argv) < 1:
    print("Usage:python3 python_scrapper URLS_FILE")
    sys.exit()

print(">> Python Scrapping")
URLS_FILE = sys.argv[1]
URLS = getAllURLS(URLS_FILE)

print(">> Reading URLS from {} found {}".format(URLS_FILE, len(URLS)))
print(">> Starting the scrapping ... ")
journals = []
for URL in URLS:
    print(">> Looking at {}".format(URL))
    (success, soup) = getPageContent(URL)
    if success == True:
        journals.append(getJournalInfo(soup))

print("\n\n")
print("# H INDEX, JOURNAL NAME, WEB PAGE")
journals.sort(key=sortFunction)
for journal in journals:
    (jname, jhindex, jhome) = journal
    print("{}\t {}\t ({})".format(jhindex, jname, jhome))


