from selenium import webdriver
import time
import datetime
from fake_useragent import UserAgent
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv
import pickle
import math

# options
options = webdriver.ChromeOptions()
useragent = UserAgent()
options.add_argument(f"User-Agent={useragent.random}")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)



iter = 1

tutiUrls = ["https://www.tutiempo.net/clima/2001/ws-345040.html","https://www.tutiempo.net/clima/2002/ws-345040.html","https://www.tutiempo.net/clima/2003/ws-345040.html",
"https://www.tutiempo.net/clima/2004/ws-345040.html","https://www.tutiempo.net/clima/2005/ws-345040.html","https://www.tutiempo.net/clima/2006/ws-345040.html",
"https://www.tutiempo.net/clima/2007/ws-345040.html","https://www.tutiempo.net/clima/2008/ws-345040.html","https://www.tutiempo.net/clima/2009/ws-345040.html",
"https://www.tutiempo.net/clima/2010/ws-345040.html","https://www.tutiempo.net/clima/2011/ws-345040.html","https://www.tutiempo.net/clima/2012/ws-345040.html",
"https://www.tutiempo.net/clima/2013/ws-345040.html","https://www.tutiempo.net/clima/2014/ws-345040.html","https://www.tutiempo.net/clima/2015/ws-345040.html",
"https://www.tutiempo.net/clima/2016/ws-345040.html","https://www.tutiempo.net/clima/2017/ws-345040.html","https://www.tutiempo.net/clima/2018/ws-345040.html",
"https://www.tutiempo.net/clima/2019/ws-345040.html","https://www.tutiempo.net/clima/2020/ws-345040.html","https://www.tutiempo.net/clima/2021/ws-345040.html",
"https://www.tutiempo.net/clima/2022/ws-345040.html"]

tutiMonth = []

script = "return window.getComputedStyle(document.querySelector('.numspan span'),':after').getPropertyValue('content')"

for url in tutiUrls:
    driver.get(url)
    for q in range(1,13):
        try:
            tutiMonth.append(driver.find_element('xpath', f'//*[@id="ColumnaIzquierda"]/div/div[6]/ul/li[{q}]/a').get_attribute("href"))
        except:
            try:
                tutiMonth.append(driver.find_element('xpath', f'//*[@id="ColumnaIzquierda"]/div/div[4]/ul/li[{q}]/a').get_attribute("href"))
            except:
                pass

def executeScript(script):
    return driver.execute_script(script)


infopermonth = []
for url in tutiMonth:
    driver.get(url)
    """time.sleep(5)"""
    try:
        for row in range(2,33):
            
            try:
                infopermonth.append({
                    'Dia': driver.find_element('xpath', f'//*[@id="ColumnaIzquierda"]/div/div[4]/table/tbody/tr[{row}]/td[1]/strong').text,
                    'T': driver.find_element('xpath',f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[2]').text,
                    'TM': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[3]').text,
                    'Tm': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[4]').text,
                    'SLP': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[5]').text,
                    'H': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[6]').text,
                    'PP': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[7]').text,
                    'VV': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[8]').text,
                    'V': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[9]').text,
                    'VM': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[10]').text,
                    'VG': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[11]').text,
                    'RA': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[12]').text,
                    'SN': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[13]').text,
                    'TS': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[14]').text,
                    'FG': driver.find_element('xpath', f'/html/body/div[4]/div[5]/div[1]/div/div[4]/table/tbody/tr[{row}]/td[15]').text,
                })
                
                #ColumnaIzquierda > div > div.mt5.minoverflow.tablancpy > table > tbody > tr:nth-child(7) > td:nth-child(2) > span.ntpq
            except: pass
            print(infopermonth)
        with open(f'tuti{iter}.csv', 'w', newline='', encoding="utf-8") as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(['Dia', 'T', 'TM', 'Tm', 'SLP', 'H', 'PP', 'VV', 'V', 'VM', 'VG', 'RA', 'SN', 'TS', 'FG'])
                for info in infopermonth:
                    writer.writerow([info['Dia'], info['T'],info['TM'], info['Tm'],info['SLP'], info['H'],info['PP'], info['VV'],info['V'], 
                    info['VM'],info['VG'], info['RA'],info['SN'], info['TS'],info['FG']])
        iter+=1
    except: pass
    




