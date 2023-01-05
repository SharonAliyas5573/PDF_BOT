from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import lxml
import time
import re
PATH="C:\Program Files (x86)\chromedrver.exe"

key=input("Enter Pdf Name:")

key = re.sub('\s+', '+', key)

website_url="https://www.pdfdrive.com/search?q="+key+"&pagecount=&pubyear=&searchin=&em="


response =requests.get(website_url)
soup = BeautifulSoup(response.text,'lxml')

Head =soup.find_all("h2")
for i in range(0,len(Head)):
    Head [i]= Head[i].get_text()


    
info =soup.find_all("div", {"class": "file-info"})

for i in range(0,len(info)):
    info [i]= info[i].get_text()

info =  ['-'.join(x.replace('\n', '').split('·')[:-1]) for x in info]


 
data = {}
for key, value in zip(Head, info):
    data[key] = value

for index, (key, value) in enumerate(data.items()):
    print(f'{index+1}. {key}: {value}\n')


links =soup.find_all("a",{"class":"ai-search"})
link=[]
for i in links:
    link.append(i['href'])
    
INDEX_NO=int(input("Select BOOK wanted :"))
INDEX_NO = (INDEX_NO-1)

dwnld_link=link[INDEX_NO]

dwnld_link="https://www.pdfdrive.com"+dwnld_link

response_1=requests.get(dwnld_link)


soup1 = BeautifulSoup(response_1.text,'lxml')

dwnld_link_2=soup1.find_all("a",{"id":"download-button-link"})

for i in dwnld_link_2:
    dwnld_link_2=i['href']

dwnld_link_2="https://www.pdfdrive.com"+dwnld_link_2

driver = webdriver.Chrome()
driver.get(dwnld_link_2)


button = driver.find_element(By.CLASS_NAME, 'btn-user')

button.click()
# html_source = driver.page_source

# soup2= BeautifulSoup(html_source, 'lxml')

# dwnld_link_3=soup2.find_all("a",{"id":"btn btn-primary btn-user"})

# for i in dwnld_link_3:
#     dwnld_link_3=i['href']



