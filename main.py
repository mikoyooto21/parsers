#from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import time
from selenium import webdriver
from fake_useragent import UserAgent
import auth_data

useragent = UserAgent()

chromeOptions = webdriver.ChromeOptions()
#chromeOptions.add_argument("--proxy-server=%s" % PROXY)
#chromeOptions.add_argument("--disable-notifications")
#chromeOptions.add_argument("--headless")
chromeOptions.add_argument(f"User-Agent={useragent.random}")
'''
proxyOptions = {
    "proxy": {
        "https":
    }
}
'''
driver = webdriver.Chrome(options=chromeOptions)
try:
    driver.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent")
    time.sleep(5)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
'''
html = driver.find_element(By.TAG_NAME, "html")
for i in range(100000):
    html.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
elems = driver.find_element(By.CSS_SELECTOR, "ul.catalog-grid").find_elements(By.CSS_SELECTOR, "span.goods-tile__title")
for elem in elems:
    print(elem.text)
cookies = driver.get_cookies()

driver.add_cookie({'name':'',
                   'value':'',
                   'domain':'',
                   'expiry':'',
                   'httpOnly':True,
                   'path':'/',
                   'secure':False,
                   })
'''
#time.sleep(10)

#html = driver.page_source
#print(html)

#driver.close()
#driver.quit()