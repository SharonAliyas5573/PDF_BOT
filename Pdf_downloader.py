from bs4 import BeautifulSoup
import requests
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import lxml
import time
import re


# Get the file name from the user
key = input("Enter Pdf Name:")

# Replace spaces with '+' in the file name
key = re.sub('\s+', '+', key)

# Set the base URL of the website
web_link = "https://www.pdfdrive.com"

# Set the search URL
website_url = "https://www.pdfdrive.com/search?q=" + \
    key+"&pagecount=&pubyear=&searchin=&em="

#  Send a request to the search URL
response = requests.get(website_url)

# Parse the HTML content
soup = BeautifulSoup(response.text, 'lxml')

# Find all the book titles
Head = soup.find_all("h2")

# Extract the text from the titles
for i in range(0, len(Head)):
    Head[i] = Head[i].get_text()

# Find all the file info elements
info = soup.find_all("div", {"class": "file-info"})

# Extract the text from the file info elements
for i in range(0, len(info)):
    info[i] = info[i].get_text()

# Clean up the file info text
info = ['-'.join(x.replace('\n', '').split('·')[:-1]) for x in info]

# Create a dictionary to store the book titles and file info
data = {}
for key, value in zip(Head, info):
    data[key] = value

# Print the book titles and file info
for index, (key, value) in enumerate(data.items()):
    print(f'{index+1}. {key}: {value}\n')

# Find all the download links
links = soup.find_all("a", {"class": "ai-search"})

# Extract the download links
link = []
for i in links:
    link.append(i['href'])

# Get the index of the book that the user wants to download
INDEX_NO = int(input("Select BOOK wanted :"))
INDEX_NO = (INDEX_NO-1)

# Get the download link for the selected book
dwnld_link = link[INDEX_NO]

# Construct the full download link
dwnld_link = web_link+dwnld_link

# Send a request to the download page
response_1 = requests.get(dwnld_link)

# Parse the HTML content
soup1 = BeautifulSoup(response_1.text, 'lxml')

# Find the download link
dwnld_link_2 = soup1.find_all("a", {"id": "download-button-link"})

# Extract the download link
for i in dwnld_link_2:
    dwnld_link_2 = i['href']

# Construct the full download link
dwnld_link_2 = web_link+dwnld_link_2

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 1}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)


# Navigate to the download page
driver.get(dwnld_link_2)

# Wait for the page to load
driver.implicitly_wait(15)

# Get the HTML source of the page
html = driver.page_source

# Close the driver
driver.close()

# Parse the HTML content
soup2 = BeautifulSoup(html, 'lxml')

# Find the download button
divs = soup2.find_all("div", {"class": "text-center"})

# Check if the book is available for download
href = ""
if divs == None:
    print("\n BOOK NOT AVAILABLE !")
    exit()
else:
    for div in divs:
        links = div.find_all('a')
        for link in links:
            href = link['href']
    if href == "":
        print("BOOK NOT AVAILABELE")
        exit()
# Construct the full download link
    if href.startswith('\/'):
        final_link = web_link+href
    else:
        final_link = href
    
    file_name = input("Enter the name for the downloaded file: [press Enter to set Defualt] ")
    if file_name=="":
        file_name="Ebook.pdf"
    else:
        file_name=file_name+'.pdf'
# set the download path to defualt downloads  folder
    file_path = os.path.join(os.path.expanduser("~"), "Downloads", file_name)
# Download the file
    urllib.request.urlretrieve(final_link, file_path)
    print(f"File downloaded and saved as {file_path}")
