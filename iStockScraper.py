import requests
from bs4 import BeautifulSoup
import urllib.request
import os

url = "https://www.istockphoto.com/hk/圖片/soda-cans?mediatype=photography&phrase=soda%20cans&sort=mostpopular"

source_code = requests.get(url)

plain_text = source_code.text

soup = BeautifulSoup(plain_text)

images = soup.find_all("a", {"class": "gallery-mosaic-asset__link"})

i = 0
for link in images:
    '''img = link.extract()
    img = img.find("figure")
    img = img.find("img")'''
    href = link.extract().find("figure").find("img").get('src')
    print(href)

    full_name = "C:/Users/Vikram Krishna/OneDrive/Desktop/Programming/recyclingVision/downloads/drink can single/" + str(i) + ".jpg"
    urllib.request.urlretrieve(href, full_name)
    i += 1

'''number = 0

for image in images:
    image_src = image["src"]
    urllib.request.urlretrieve((image_src), str(number))
    number += 1'''

print("All completed!")