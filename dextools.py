import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

urls = set()

def collect_links(driver, chain):
    driver.get(chain)
    driver.maximize_window()
    time.sleep(1)

    try:
        driver.find_element(By.CLASS_NAME, "fa-xmark").click()
        print("Clicked X")
    except:
        pass

    time.sleep(3)
    try:
        element = driver.find_element(By.XPATH, "/html/body/app-root/div/div/main/app-new-home/app-layout/div/div[2]")
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print("Scrolled down")
    except:
        pass

    try:
        pagination_button = driver.find_element(By.XPATH, '//*[@id="pairs"]/ngx-datatable/div/datatable-footer/div/div/button/span')
    except:
        elements = driver.find_elements(By.XPATH, '//*[@id="pairs"]/ngx-datatable/div/datatable-body/datatable-selection/datatable-scroller/*/datatable-body-row/div[1]/datatable-body-cell/div/div/div[1]/a')
        for element in elements:
            url = element.get_attribute("href")
            if url is not None:
                urls.add(url)

        print(len(urls))
        return urls

    while True:
        elements = driver.find_elements(By.XPATH, '//*[@id="pairs"]/ngx-datatable/div/datatable-body/datatable-selection/datatable-scroller/*/datatable-body-row/div[1]/datatable-body-cell/div/div/div[1]/a')
        for element in elements:
            url = element.get_attribute("href")
            if url is not None:
                urls.add(url)

        print(len(urls))

        try:
            if pagination_button is None:
                return urls
            pagination_button.click()
            print("Clicked NEXT")
            time.sleep(1)
            pagination_button = driver.find_element(By.CSS_SELECTOR, '#pairs > ngx-datatable > div > datatable-footer > div > div > button:nth-child(3) > span')
        except NoSuchElementException:
            return urls

def collect_data(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'app-token-name')))
    except Exception as e:
        print(f"Error processing URL: {url}")
        print(str(e))
        return

    try:
        token_name = driver.find_element(By.TAG_NAME, 'app-token-name').find_element(By.XPATH, 'span/span[1]').text
        token_pair = driver.find_element(By.TAG_NAME, 'app-token-name').find_element(By.XPATH, 'span/span[3]').text
    except:
        token_name = ''
        token_pair = ''

    print(token_name, token_pair)

    try:
        element = driver.find_element(By.XPATH, "/html/body/app-root/div/div/main/app-new-home/app-layout/div/div[2]")
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print("Scrolled down")
    except:
        pass

    try:
        description = driver.find_element(By.TAG_NAME, 'app-token-description').find_element(By.XPATH, "div/div[*]/span").text
    except:
        description = ''

    print(description)

    try:
        driver.find_element(By.XPATH, '/html/body/app-root/div/div/main/app-pairexplorer/app-layout/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/a[2]').click()
        time.sleep(0.7)
        links_left = driver.find_elements(By.XPATH, '/html/body/ngb-modal-window/div/div/app-links-social-modal/div[2]/div/div/*/*/*')

        link_list = [link_url.get_attribute("href") for link_url in links_left]
        if link_list == [] or link_list == [None]:
            links_one = driver.find_elements(By.XPATH, '/html/body/app-root/div/div/main/app-pairexplorer/app-layout/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/*')
            link_list = [link_url.get_attribute("href") for link_url in links_one]
            links_two = driver.find_elements(By.XPATH, '/html/body/app-root/div/div/main/app-pairexplorer/app-layout/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/*/*')

            link_list.extend([link_url.get_attribute("href") for link_url in links_two])
    except:
        links_one = driver.find_elements(By.XPATH, '/html/body/app-root/div/div/main/app-pairexplorer/app-layout/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/*')
        link_list = [link_url.get_attribute("href") for link_url in links_one]
        links_two = driver.find_elements(By.XPATH, '/html/body/app-root/div/div/main/app-pairexplorer/app-layout/div/div/div/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/div/*/*')
        link_list.extend([link_url.get_attribute("href") for link_url in links_two])

    print(link_list)

    fieldnames = ["Token Name", "Token Pair", "Links", "Description"]

    with open('data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow({
            "Token Name": token_name,
            "Token Pair": token_pair,
            "Links": link_list,
            "Description": description
        })

driver = webdriver.Chrome()

chains = ['https://www.dextools.io/app/en/ether/pairs', 'https://www.dextools.io/app/en/bnb/pairs',
          'https://www.dextools.io/app/en/arbitrum/pairs', 'https://www.dextools.io/app/en/polygon/pairs',
          'https://www.dextools.io/app/en/aptos/pairs', 'https://www.dextools.io/app/en/solana/pairs',
          'https://www.dextools.io/app/en/fantom/pairs', 'https://www.dextools.io/app/en/avalanche/pairs',
          'https://www.dextools.io/app/en/cronos/pairs', 'https://www.dextools.io/app/en/multiversx/pairs',
          'https://www.dextools.io/app/en/okc/pairs', 'https://www.dextools.io/app/en/ethergoerli/pairs',
          'https://www.dextools.io/app/en/pulse/pairs', 'https://www.dextools.io/app/en/heco/pairs',
          'https://www.dextools.io/app/en/velas/pairs', 'https://www.dextools.io/app/en/aurora/pairs',
          'https://www.dextools.io/app/en/harmony/pairs', 'https://www.dextools.io/app/en/moonbeam/pairs',
          'https://www.dextools.io/app/en/oasis/pairs', 'https://www.dextools.io/app/en/kucoin/pairs',
          'https://www.dextools.io/app/en/astar/pairs', 'https://www.dextools.io/app/en/celo/pairs',
          'https://www.dextools.io/app/en/fuse/pairs', 'https://www.dextools.io/app/en/moonriver/pairs',
          'https://www.dextools.io/app/en/optimism/pairs', 'https://www.dextools.io/app/en/iotex/pairs',
          'https://www.dextools.io/app/en/klaytn/pairs', 'https://www.dextools.io/app/en/telos/pairs',
          'https://www.dextools.io/app/en/milkomeda/pairs', 'https://www.dextools.io/app/en/dfk/pairs',
          'https://www.dextools.io/app/en/evmos/pairs', 'https://www.dextools.io/app/en/etc/pairs',
          'https://www.dextools.io/app/en/bitgert/pairs', 'https://www.dextools.io/app/en/arbitrumnova/pairs',
          'https://www.dextools.io/app/en/redlight/pairs', 'https://www.dextools.io/app/en/canto/pairs',
          'https://www.dextools.io/app/en/echelon/pairs', 'https://www.dextools.io/app/en/kardia/pairs',
          'https://www.dextools.io/app/en/tomb/pairs', 'https://www.dextools.io/app/en/conflux/pairs',
          'https://www.dextools.io/app/en/smartbch/pairs', 'https://www.dextools.io/app/en/shiden/pairs',
          'https://www.dextools.io/app/en/boba/pairs', 'https://www.dextools.io/app/en/elastos/pairs',
          'https://www.dextools.io/app/en/wan/pairs', 'https://www.dextools.io/app/en/rsk/pairs',
          'https://www.dextools.io/app/en/gnosis/pairs', 'https://www.dextools.io/app/en/nova/pairs',
          'https://www.dextools.io/app/en/cube/pairs', 'https://www.dextools.io/app/en/syscoin/pairs',
          'https://www.dextools.io/app/en/ronin/pairs', 'https://www.dextools.io/app/en/fusion/pairs',
          'https://www.dextools.io/app/en/kava/pairs', 'https://www.dextools.io/app/en/hoo/pairs',
          'https://www.dextools.io/app/en/tomo/pairs', 'https://www.dextools.io/app/en/thundercore/pairs',
          'https://www.dextools.io/app/en/meter/pairs', 'https://www.dextools.io/app/en/kek/pairs',
          'https://www.dextools.io/app/en/ethf/pairs', 'https://www.dextools.io/app/en/sx/pairs',
          'https://www.dextools.io/app/en/muu/pairs', 'https://www.dextools.io/app/en/shib/pairs',
          'https://www.dextools.io/app/en/alvey/pairs', 'https://www.dextools.io/app/en/dogechain/pairs',
          'https://www.dextools.io/app/en/flare/pairs', 'https://www.dextools.io/app/en/pom/pairs',
          'https://www.dextools.io/app/en/ultron/pairs', 'https://www.dextools.io/app/en/energi/pairs',
          'https://www.dextools.io/app/en/exosama/pairs', 'https://www.dextools.io/app/en/coredao/pairs',
          'https://www.dextools.io/app/en/ethw/pairs', 'https://www.dextools.io/app/en/filecoin/pairs',
          'https://www.dextools.io/app/en/zksync/pairs', 'https://www.dextools.io/app/en/polygonzkevm/pairs',
          'https://www.dextools.io/app/en/metis/pairs']

all_urls = set()

for chain in chains:
    urls = collect_links(driver, chain)
    all_urls.update(urls)

for url in all_urls:
    collect_data(driver, url)

driver.quit()