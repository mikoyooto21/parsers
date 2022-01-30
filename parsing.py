from selenium import webdriver
import time
import datetime
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
import csv
import pickle
from multiprocessing import Pool
import math

# options
options = webdriver.ChromeOptions()

useragent = UserAgent()

options.add_argument(f"User-Agent={useragent.random}")

options.add_argument("--disable-blink-features=AutomationControlled")

# headless mode
# options.add_argument("--headless")
# options.headless = True

driver = webdriver.Chrome(options=options)

guidesInfo = []
try:
    start_time = datetime.datetime.now()

    driver.get("https://www.bmg.org.uk/find-a-guide/?loc=&dir=ASC")

    for cookie in pickle.load(open(f"guide_cookies", "rb")):
        driver.add_cookie(cookie)
    time.sleep(1)
    driver.refresh()

    #pickle.dump(driver.get_cookies(), open(f"guide_cookies", "wb"))
    time.sleep(5)
    urls = []
    for i in range(1, 142):
        urls.append(driver.find_element("xpath", f"/html/body/div[4]/ul/li[{i}]/a").get_attribute("href"))
    print(urls)

    for url in urls:
        driver.get(url)

        #Name
        first_name = []
        last_name = []
        first_name.append(driver.find_element("xpath", "/html/body/div[1]/div[1]/div[1]/h1").text.split(' ')[0])
        last_name.append(driver.find_element("xpath", "/html/body/div[1]/div[1]/div[1]/h1").text.split(' ')[1])

        #activities
        activities_main = []
        activities = driver.find_elements("xpath", "/html/body/div[1]/div[3]/div/ul/*")
        s = 1
        for i in activities:
            activities_main.append(driver.find_element("xpath", f"/html/body/div[1]/div[3]/div/ul/li[{s}]/a").text)
            s+=1

        #description
        description = []
        description.append(driver.find_element("xpath", "/html/body/div[1]/div[1]/div[1]/div[3]").text)

        #social media links
        social = []
        social_links = driver.find_elements("xpath", "/html/body/div[1]/div[1]/div[2]/ul/*")
        q = 1
        for i in social_links:
            try:
                social.append(driver.find_element("xpath", f"/html/body/div[1]/div[1]/div[2]/ul/li[{q}]/a").get_attribute('href'))
                q+=1
            except:
                try:
                    social.append(driver.find_element("xpath", "/html/body/div[1]/div[1]/div[2]/ul/li/a").get_attribute('href'))
                except:
                    pass


        #contacts
        contats = driver.find_elements("xpath", "/html/body/div[1]/*/ul")
        c = 1
        contats2 = []
        for i in contats:
            try:
                contats2.append(driver.find_element("xpath", f"/html/body/div[1]/*/ul/li[1]/a[{c}]").get_attribute("href"))
                contats2.append(driver.find_element("xpath", f"/html/body/div[1]/*/ul/li[2]/a[{c}]").get_attribute("href"))
                for s in range(6):
                    try:
                        contats2.append(driver.find_element("xpath", f"/html/body/div[1]/*/ul/li[3]/a[{c}]").get_attribute("href"))
                        c += 1
                    except:
                        pass
            except:
                pass
        try:
            x = contats2.index('')
            contats2.pop(x)
        except:
            pass

        email = []
        phone_number = []
        sites = []
        for item in contats2:
            if item.split(":")[0]=="mailto":
                email.append(item)
            elif item.split(":")[0]=="tel":
                phone_number.append(item)
            else:
                sites.append(item)

        guidesInfo.append({
            'first_name': ",".join(first_name),
            'last_name': ",".join(last_name),
            'activities': ",".join(activities_main),
            'description': ",".join(description),
            'social': ",".join(social),
            'email': ",".join(email),
            'phone': ",".join(phone_number),
            'sites': ",".join(sites)
            })

    print(guidesInfo)

    #saveing
    with open('guides.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['First_Name', 'Las_Name', 'activities', 'description', 'social_media_links', 'mail', 'phone', 'sites'])
        for guide in guidesInfo:
            writer.writerow([guide['first_name'], guide['last_name'], guide['activities'], guide['description'],
                             guide['social'], guide['email'], guide['phone'], guide['sites']])

    time.sleep(20)

    print()

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
