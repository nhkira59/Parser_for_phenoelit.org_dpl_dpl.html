import requests
from bs4 import BeautifulSoup
import csv

URL = 'http://www.phenoelit.org/dpl/dpl.html'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
           'Accept': '*/*'}
PATH = "output.csv"


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr')
    table_rows = []
    for item in items:
        table_rows.append([
            item.find('td').get_text(),  # Vendor
            item.find('td').find_next('td').get_text(),  # Model
            item.find('td').find_next('td').find_next('td').get_text(),  # Version
            item.find('td').find_next('td').find_next('td').find_next('td').get_text(),  # Access Type
            item.find('td').find_next('td').find_next('td').find_next('td').find_next('td').get_text(),  # Username
            item.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').get_text(),
            # Password
            item.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next(
                'td').get_text(),  # Privileges
            item.find('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next('td').find_next(
                'td').find_next('td').get_text(),  # Notes
        ])
    return table_rows


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        return get_content(html.text)
    else:
        print('Нет интернет соединения, проверьте подключение.')


def csv_writer(data, path):
    """
    Функция для записи данных в CSV
    """
    with open(path, "w", newline='') as csv_file:
        '''
        csv_file - объект с данными
        delimiter - разделитель
        '''
        writer = csv.writer(csv_file, delimiter=';')
        for line in data:
            writer.writerow(line)
    print('Записано в файл.')


csv_writer(parse(), PATH)
