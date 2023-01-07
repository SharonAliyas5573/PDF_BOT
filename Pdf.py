from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import lxml
import time
import re


os.environ['webdriver.chrome.driver'] = "C:\Program Files (x86)\chromedrver.exe"


# Get the file name from the user
key = input("Enter Pdf Name:")

# Replace spaces with '+' in the file name
key = re.sub('\s+', '+', key)

# Set the base URL of the website
web_link="https://www.pdfdrive.com"

# Set the search URL
website_url = "https://www.pdfdrive.com/search?q=" +key+"&pagecount=&pubyear=&searchin=&em="

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

#Create a dictionary to store the book titles and file info
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
INDEX_NO =(INDEX_NO-1)

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

capabilities = DesiredCapabilities().CHROME
capabilities['acceptInsecureCerts'] = True

driver = webdriver.Chrome(desired_capabilities=capabilities)

# # Set up the Chrome driver options
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')

# # Create a Chrome driver instance
# driver = webdriver.Chrome(chrome_options=options)

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
        links = div.find_all('a', {'class':'btn btn-primary btn-user'})
        for link in links:
            href = link['href']
            
# Construct the full download link
    final_link =web_link+href
# Set the downloads folder
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
# Set the file name
    FILE_NAME=Head[INDEX_NO]
    words = FILE_NAME.split()
    FILE_NAME = words[:5]
    FILE_NAME = " ".join(FILE_NAME)

# Set the file path
    file_path = os.path.join(downloads_folder,(FILE_NAME+".pdf"))
# Send a request to download the file
    response = requests.get(final_link)

# Check if the  file is available
    if href !="":
        if response.content:

    # Save the file
            with open(file_path, "wb") as f:
        # Write the data to the file
                f.write(response.content)
   

            print("SUCCESSFULLY DOWNLOADED")
        else:
            print("BOOK NOT AVAILABLE")
    else:
            print("BOOK NOT AVAILABLE")
