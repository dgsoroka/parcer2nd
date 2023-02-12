import sys

import re
import xlsxwriter  # pip install XlsxWriter
import requests  # pip install requests
from bs4 import BeautifulSoup as bs  # pip install beautifulsoup4

headers = {'accept': '/',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/71.0.3578.98 Safari/537.36'}
base_url = 'https://www.mealberry.ru/catalog/?brand[]=336&type[]=604&keepTypes=Y'

food = []
textWeight = []
textArticle = []


def mealberry_parse(base_url, headers):
    global end_with, start_with
    zero = 0
    # while pages > zero:
    zero = str(zero)
    session = requests.Session()
    request = session.get(base_url, headers=headers)

    workbook = xlsxwriter.Workbook('Result.xlsx')
    worksheet = workbook.add_worksheet()

    # Настройка ширины колонок
    worksheet.set_column(0, 0, 35)  # A  https://xlsxwriter.readthedocs.io/worksheet.html#set_column
    worksheet.set_column(1, 1, 20)  # B
    worksheet.set_column(2, 2, 40)  # C

    worksheet.write('A1', 'Наименование')
    worksheet.write('B1', 'Вес')
    worksheet.write('C1', 'Артикль')

    row = 1
    col = 0
    count = 0

    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'class': 'col-lg-4 col-sm-6 col-xxs-12 col-padd-clear card-list-item'})
        for div in divs:
            title = div.find('a', attrs={'data-type': 'text-ellipsis'}).text
            weights = div.find_all('div', attrs={'class': 'text'})
            articles = div.find_all('div', attrs={'class': 'value'})
            for weight in weights:
                textWeight.append(weight.find(text=re.compile(r'\d+\b')))
            for article in articles:
                textArticle.append(article.find(text=re.compile(r'\d+\b')))
            if 'хом' in title:
                print(textArticle)
                print(textWeight)
                print(title)

                worksheet.write_string(row, col, title)
                row += 1
                while count < len(textWeight):
                    worksheet.write_string(row, col + 1, textWeight[count])
                    worksheet.write_string(row, col + 2, textArticle[count])
                    row += 1
                    count += 1
                row += 2

            count = 0
            textArticle.clear()
            textWeight.clear()
    workbook.close()


mealberry_parse(base_url, headers)
