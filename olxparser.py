from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time

# options
options = webdriver.ChromeOptions()

useragent = UserAgent()

options.add_argument(f"{useragent}")

options.add_argument("--disable-blink-features=AutomationControlled")

# headless mode
# options.add_argument("--headless")
# options.headless = True

driver = webdriver.Chrome(options=options)

driver.get("https://www.olx.ua/transport/legkovye-avtomobili/")

# count pages
pages = driver.find_elements(By.CSS_SELECTOR, "#body-container > div:nth-child(3) > div > div.pager.rel.clr > * > a")
urls = []
for page in pages:
    urls.append(page.get_attribute("href"))
urls.pop(-1)
url = urls[-1]
page_number = url.split("=")[1]
main_url = url.replace(page_number, "")
acc_urls = []

names = []
phones = []
try:
    # getting all pages
    for i in range(1, int(page_number)+1):
        driver.get(main_url+str(i))

        cars = driver.find_elements(By.CLASS_NAME, "marginright5.link.linkWithHash.detailsLink")
        for car in cars:
            acc_urls.append(car.get_attribute("href"))
    for url in acc_urls:
        driver.get(url)
        #name
        names.append(driver.find_element(By.CSS_SELECTOR, ".css-u8mbra-Text.eu5v0x0").text)

        #phone
        try:
            driver.find_element("xpath", "//*[@id='root']/div[1]/div[3]/div[3]/div[2]/div[1]/div[2]/*").click()
            time.sleep(5)
            phones.append(driver.find_element("xpath", "//*[@id='root']/div[1]/div[3]/div[3]/div[1]/div[4]/div/div/div/ul/li").text)
        except:
            pass
    print(acc_urls.count(), names.count(), phones.count())

    time.sleep(20)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
