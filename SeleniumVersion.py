from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re


moduleLink = 'https://moodle.nottingham.ac.uk/course/view.php?id=33554'

browser = webdriver.Chrome()

download_dir = "F:\\Users" # for linux/*nix, download_dir="/usr/Public"
options = webdriver.ChromeOptions()

profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": download_dir , "download.extensions_to_open": "applications/pdf"}
options.add_experimental_option("prefs", profile)
browser = webdriver.Chrome(chrome_options=options)  # Optional argument, if not specified will search path.
browser.get('https://moodle.nottingham.ac.uk/login/index.php')
wait = WebDriverWait(browser, 10)
	
user = wait.until(EC.presence_of_element_located((By.ID,'username')))
pas = wait.until(EC.presence_of_element_located((By.ID,'password')))
btn = wait.until(EC.presence_of_element_located((By.ID,'loginbtn')))

user.send_keys('zy15760')
pas.send_keys('App995828?!')
btn.click()
browser.implicitly_wait(10)

print(type(browser.get_cookies()))
browser.get(moduleLink)

#print(type(browser.page_source))

soup = BeautifulSoup(browser.page_source, 'lxml')
pdfs = []
for link in soup.find_all(name = 'a', attrs={'href':re.compile('.*pdf$')}):
	pdfs.append(link['href'])
	
	
for url in pdfs:
	browser.get(url)
	
	
	
	
	

