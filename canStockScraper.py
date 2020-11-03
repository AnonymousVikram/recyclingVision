import time
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

DRIVER_PATH = 'C:/Windows/chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://www.canstockphoto.com/images-photos/soda-cans.html")

start = time.time()
while time.time() <= start + 15:
    driver.execute_script("window.scrollBy(0, 1000)");

source_code = driver.page_source
driver.quit()

print("Completed Selenium")

plain_text = source_code

soup = BeautifulSoup(plain_text)

images = soup.find_all("article")

i = 0
for link in range(len(images)-1):
    href = images[link].extract().find("a").find("img").get("src")
    print(href)

    full_name = "C:/Users/Vikram Krishna/OneDrive/Desktop/Programming/recyclingVision/downloads/drink can single/CanPhotos" + str(
        i) + ".jpg"
    urllib.request.urlretrieve(href, full_name)
    i += 1
