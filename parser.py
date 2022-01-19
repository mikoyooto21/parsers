import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/uk/newauto/marka-mitsubishi/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50', 'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'

def get_html(url, params=None):
	r = requests.get(url, headers=HEADERS, params=params)
	return r

def get_pages_count(html):
	soup = BeautifulSoup(html, 'html.parser')
	pagination = soup.find_all('span', class_='mhide')
	if pagination:
		return int(pagination[-1].get_text())
	else:
		return 1

def get_content(html):
	soup = BeautifulSoup(html, 'html.parser')
	items = soup.find_all('section', class_='proposition')
	cars = []
	for item in items:
		uah = item.find('span', class_='size16')
		if uah:
			uah = uah.get_text()
		else:
			uah = 'Цену уточнить'
		cars.append({
			'title': item.find('div', class_='proposition_title').get_text(strip=True),
			'link': HOST + item.find('a', class_='proposition_link').get('href'),
			'dollars': item.find('span', class_='green').get_text(strip=True),
			'uah': uah,
			'city': item.find('span', class_='item region').get('title')

		})
	return cars

def save_file(items, path):
	with open(path, 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Марка', 'Ссылка', 'Доллары', 'Гривны', 'Город'])
		for item in items:
			writer.writerow([item['title'], item['link'], item['dollars'], item['uah'], item['city']])

def parse():
	URL = input('Enter URL: ')
	URL = URL.strip()
	html = get_html(URL)
	if html.status_code == 200:
		cars = []
		pages_count = get_pages_count(html.text)
		for page in range(1, pages_count + 1):
			print(f'Парсинг страницы {page} из {pages_count}...')
			html = get_html(URL, params={'page': page})
			cars.extend(get_content(html.text))
		save_file(cars, FILE)
		print(f'Received {len(cars)} cars')
		os.startfile(FILE)
	else:
		print('Error')


parse()