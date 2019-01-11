from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as E
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
br = webdriver.Chrome(chrome_options=chrome_options)

url = "https://project-portal.doc.ic.ac.uk/login"
wait = WebDriverWait(br, 20)

br.get(url)
username = wait.until(E.presence_of_element_located((By.XPATH, '//*[@id="App"]/div/div[2]/div/div/div[2]/form/div[1]/input')))
pw = wait.until(E.presence_of_element_located((By.XPATH,'//*[@id="App"]/div/div[2]/div/div/div[2]/form/div[2]/input')))
btn = wait.until(E.presence_of_element_located((By.XPATH,'//*[@id="App"]/div/div[2]/div/div/div[2]/form/button')))

username.send_keys('')
pw.send_keys('')
btn.click()

btnII = wait.until(E.presence_of_element_located((By.XPATH, '//*[@id="App"]/div/div[2]/div/div/div/button[2]')))
btnII.send_keys(Keys.ENTER)

br.get('https://project-portal.doc.ic.ac.uk/proposal_selection')
wait.until(E.presence_of_element_located((By.XPATH, '//*[@id="App"]/div/div[2]/div/div/div[10]/table/tbody')))

s = BeautifulSoup(br.page_source, 'lxml')
items = s.find_all(class_ = 'table-responsive')[-1]
project = items.tbody.find_all(name = 'tr')
count = 0
nonechoose = 0
for i in project:
    txt = i.get_text()
    
    reg = '\[1: 0, 2: 0, 3: 0, SNR: (\d+), ALLOC: 0\]'
    result = re.search(reg, txt)
    SNR = int(result.group(1))
    if SNR == 0:
        nonechoose += 1
    count = count + SNR

print('{} projects have no students'.format(nonechoose))
print('About {} students have chosen'.format(count))
