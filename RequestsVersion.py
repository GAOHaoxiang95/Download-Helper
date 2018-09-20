import requests
from bs4 import BeautifulSoup
import re
import os
print('''1.输入自己正确的用户名和密码（和Moodle相同）
2.在浏览器中登陆moodle,进入想批量下载课件的课程页面并复制地址栏中的地址
3.输入到“课程链接”，点击回车
4.页面上所有PDF格式的课件会被下载到程序当前文件夹下\n'''
)
username = input("Username: ")
password = input("Password: ")

os.system('cls')
module = input("课程链接: ")

print("程序处理中... ...")
#module = 'https://moodle.nottingham.ac.uk/course/view.php?id=33554'
s = requests.Session()

data = {'username':username, 'password':password}
s.post('https://moodle.nottingham.ac.uk/login/index.php', data = data)

r = s.get(module)
#print(r.text)
#print(r.cookies)

soup = BeautifulSoup(r.text, 'lxml')
pdfs = []

os.system('cls')
print("正在获取有效链接... ...")
n = 0

for link in soup.find_all(name = 'a', attrs={'href':re.compile('.*pdf$')}):
	print(link['href'])
	pdfs.append(link['href'])
	n += 1


for link in soup.find_all(name = 'a', attrs={'href':re.compile('^https://moodle\.nottingham\.ac\.uk/mod/resource/view.*')}):
	#print(link['href'])
	r = s.get(link['href'])
	innerSoup = BeautifulSoup(r.text, 'lxml')
	for innerLink in innerSoup.find_all(name = 'a', attrs={'href':re.compile('.*pdf$')}):
		pdfs.append(innerLink['href'])
		print(innerLink['href'])
		n += 1
		
i = 0
for url in pdfs:
	#print(url)
	i+=1
	fileName = url.split('/')[-1]
	os.system('cls')
	print("下载进度：{}/{}... ...\n\nCtrl + C中断程序".format(i, n))
	#print(fileName)
	r = s.get(url)
	with open(fileName, 'wb') as f:
		f.write(r.content)
#print(pdfs)
