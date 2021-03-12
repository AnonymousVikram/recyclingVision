import time
#import urllib.request

import requests
import shutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = '/Users/anonymousvikram/chromedriver'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.flickr.com/search/?text=soda%20can&view_all=1")

time.sleep(5)
driver.execute_script("window.scrollBy(0, 100)")

if(len(driver.find_elements_by_xpath("//button[@id='truste-consent-button']")) != 0):
    print("Found button")
    driver.find_element_by_xpath("//button[@id='truste-consent-button']").click()
    print("Agreed")

time.sleep(10)

start = time.time()

imageLeads = []

print("starting")
sources = []

counter = 0

while time.time() <= start + 300:
    driver.execute_script("window.scrollBy(0, 12000)")

    print("Scroll")

    time.sleep(0.5)

    if(len(driver.find_elements_by_xpath("//button[@class='alt']")) != 0):
            driver.find_element_by_xpath("//button[@class='alt']").click()
            print("load more")

    if(len(driver.find_elements_by_xpath("//button[@class='alt no-outline']")) != 0):
        driver.find_element_by_xpath("//button[@class='alt no-outline']").click()
        print("load more")
    
    counter = counter + 1
    
    if(counter == 5):
        print("Loading pictures now")

        time.sleep(15)

        print("Done Loading")

        print(str(time.time() - start) + " seconds")

        plainText = driver.page_source
        soupTemp = BeautifulSoup(plainText)

        imageIteration1 = soupTemp.find_all("a", {"class": "overlay"})

        for imageLead in imageIteration1:

            href = imageLead.extract().get('href')
            href = "https://www.flickr.com" + href

            isRepeat = False

            for usedLead in imageLeads:
                if(usedLead == href):
                    isRepeat = True
            
            if(isRepeat):
                print("Repeat image lead")
            else:
                print(href)
                imageLeads.append(href)
        
        print(str(len(imageLeads)) + " image leads found so far")

        counter = 0

print(str(len(imageLeads)) + " image leads found")
print("sleeping zzz")
time.sleep(10)

# source_code = driver.page_source

driver.quit()
print("Finding True Image URLs")

trueImageUrls = []

tempInt = 0

driverImg = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

for href in imageLeads:
    
    '''href = lead.extract().get('href')
    href = "https://www.flickr.com" + href'''

    driverImg.get(href)

    trueImageSource = driverImg.page_source

    trueImageSoup = BeautifulSoup(trueImageSource)

    trueImageLink = trueImageSoup.find("img")

    trueHref = trueImageLink.get("src")[2:]
    trueHref = "https://" + href
    print(str(tempInt) + "/" + str(len(imageLeads)) + ": " + href)
    trueImageUrls.append(href)
    tempInt = tempInt + 1

print(str(len(trueImageUrls)) + " true images found")
tempInt = 0
for imageUrl in trueImageUrls:
    full_name = "/Users/anonymousvikram/recyclingVision/downloads/drink can single/Flickr" + str(
            tempInt) + ".jpg"
    
    print(str(tempInt) + "/" + str(len(trueImageUrls)) + ": " + full_name[66:])

    r = requests.get(href, stream=True)
    with open(full_name, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)    
        tempInt += 1


print(str(tempInt) + " images processed")