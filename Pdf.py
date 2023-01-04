from bs4 import BeautifulSoup
import requests
import lxml
import re

key=input("Enter Pdf Name:")

key = re.sub('\s+', '+', key)

website_url="https://www.pdfdrive.com/search?q="+key+"&pagecount=&pubyear=&searchin=&em="


response =requests.get(website_url)
soup = BeautifulSoup(response.text,'lxml')
list=soup.find_all("div",{"class":"file-right"})

def listToString(list):
   
    
    names= " "
   
    
    return (names.join(list))

names =listToString(list)

# for names in list:

#     name = name.rsplit("<h2>")
    





print(names)



