import sys

import re
import xlsxwriter  # pip install XlsxWriter
import requests  # pip install requests
from bs4 import BeautifulSoup as bs  # pip install beautifulsoup4

headers = {'accept': '/',
           'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/71.0.3578.98 Safari/537.36'}
base_url = 'https://www.mealberry.ru/catalog/?brand[]=336&type[]=604&keepTypes=Y'
# pages = int(input('Укажите кол-во страниц для парсинга: '))

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
            textArticle.clear()
            textWeight.clear()

#             compensation = ""
#             # compensation = div.find('div', attrs={'data-qa': 'vacancy-salary-compensation-type-net'})
#             # if compensation == None: # Если зарплата не указана
#             #         compensation = 'None'
#             # else:
#             try:
#                 compensation = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
#                 start_end = re.findall(r'\b\d+\d', compensation)
#                 start_with = start_end[0] + start_end[1]
#             except:
#                 compensation = 'None'
#         # print(jobs)
#         zero = int(zero)
#         zero += 1
#
#     else:
#         print('error')
#         zero = int(zero)
#
#         # Запись в Excel файл
#         workbook = xlsxwriter.Workbook('Vacancy.xlsx')
#         worksheet = workbook.add_worksheet()
#         # Добавим стили форматирования
#         bold = workbook.add_format({'bold': 1})
#         bold.set_align('center')
#         center_H_V = workbook.add_format()
#         center_H_V.set_align('center')
#         center_H_V.set_align('vcenter')
#         center_V = workbook.add_format()
#         center_V.set_align('vcenter')
#         cell_wrap = workbook.add_format()
#         cell_wrap.set_text_wrap()
#
#         # Настройка ширины колонок
#         worksheet.set_column(0, 0, 35)  # A  https://xlsxwriter.readthedocs.io/worksheet.html#set_column
#         worksheet.set_column(1, 1, 20)  # B
#         worksheet.set_column(2, 2, 40)  # C
#         worksheet.set_column(3, 3, 40)  # D
#         worksheet.set_column(4, 4, 135)  # E
#
#         worksheet.write('A1', 'Наименование', bold)
#         worksheet.write('B1', 'Зарплата от', bold)
#         worksheet.write('C1', 'Зарплата до', bold)
#         worksheet.write('D1', 'Компания', bold)
#         worksheet.write('E1', 'Описание', bold)
#         worksheet.write('F1', 'Ссылка', bold)
#
#         row = 1
#         col = 0
#         for i in food:
#             worksheet.write_string(row, col, i[0], center_V)
#             worksheet.write_number(row, col + 1, i[1], center_H_V)
#             worksheet.write_number(row, col + 2, i[2], center_H_V)
#             worksheet.write_string(row, col + 3, i[3], cell_wrap)
#             # worksheet.write_url (row, col + 4, i[4], center_H_V)
#             worksheet.write_url(row, col + 4, i[4], cell_wrap)
#             worksheet.write_url(row, col + 5, i[5])
#             row += 1
#
#         print('OK')
#     # print(jobs)
#     workbook.close()
#
#
mealberry_parse(base_url, headers)
