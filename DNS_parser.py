import pickle
import pandas as pd
import sys
import os
import xml.etree.ElementTree as ElementTree
from datetime import datetime
from json import dumps
from typing import Any, Iterable, Mapping, Optional
from xml.dom.minidom import parseString

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.utils import get_column_letter
from tqdm import tqdm

from pprint import pprint
from random import randint
from time import sleep as pause
from time import time
from bs4 import BeautifulSoup
import undetected_chromedriver as uc

if not os.path.exists('resulting files'):
    os.makedirs('resulting files')


def parse_characteristics_page(driver, url):

    driver.get(url)
    pause(randint(7, 11))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #print(soup.prettify())

    name = soup.find('div', class_="product-card-description__title")
    price = soup.find('div', class_="product-buy__price")
    desc = soup.find('div', class_="product-card-description-text")
    avail = soup.find('a', class_="order-avail-wrap__link ui-link ui-link_blue")
    charcs = soup.find_all('div', class_="product-characteristics__spec-title")
    cvalue = soup.find_all('div', class_="product-characteristics__spec-value")
    main_picture = soup.find('img', class_="product-images-slider__main-img")
    pictures_soup = soup.find_all('img', class_="product-images-slider__img loaded tns-complete")

    pictures_list = []
    for i in pictures_soup:
        _ = pictures_list.append(i.get('data-src'))
        if _ is not None:
            pictures_list.append(_)

    span_tags = soup.find_all('span')
    for i in span_tags:
        if bool(str(i).find('data-go-back-catalog') != -1):
            category = i

    tech_spec = {}
    for f1, f2 in zip(charcs, cvalue):
        tech_spec[f1.text.rstrip().lstrip()] = f2.text.rstrip().lstrip()

    notebook = {}

    notebook["Категория"] = category.text.lstrip(': ')
    notebook["Наименование"] = name.text[15:]
    notebook["Цена"] = int(price.text.replace(' ', '')[:-1])
    notebook["Доступность"] = avail.text if avail is not None else 'Товара нет в наличии'
    notebook["Ссылка на товар"] = url
    notebook["Описание"] = desc.text
    notebook["Главное изображение"] = main_picture.get('src')
    notebook["Лист с картинками"] = pictures_list
    notebook["Характеристики"] = list(tech_spec.items())

    for i, j in notebook.items():
        print(i, j)

    return notebook


def get_date_and_time() -> str:
    return datetime.now().strftime('%d.%m.%y %H-%M-%S')


def get_all_notebook_urls(driver):
    page = 10
    url_template = 'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?f[p3q]=b3ci&p={page}'
    #url_template = 'https://www.dns-shop.ru/catalog/17a89bb916404e77/platy-rasshireniya/?p={page}'

    url = url_template.format(page=page)
    driver.get(url=url)
    pause(10)

    urls = []
    while page_urls := get_urls_from_page(driver):
        print(f'Страница {page}')

        urls.extend(page_urls)

        url = url_template.format(page=page)

        page += 1

        driver.get(url)
        pause(randint(6, 9))

    return urls


def get_urls_from_page(driver):
    """
    Собирает все ссылки на ноутбуки из текущей страницы.
    """
    soup = BeautifulSoup(driver.page_source, 'lxml')
    elements = soup.find_all('a', class_="catalog-product__name ui-link ui-link_black")
    return list(map(
        lambda element: 'https://www.dns-shop.ru' + element.get("href") + 'characteristics/',
        elements
    ))


def to_excel(data, column_names, file_name="table"):

    workbook = Workbook()
    sheet = workbook.active
    print('=' * 20)



    side = Side(border_style='thin')
    border = Border(
        left=side,
        right=side,
        top=side,
        bottom=side
    )
    alignment = Alignment(
        horizontal='center',
        vertical='center'
    )
    column_widths = []

    for column, name in enumerate(column_names, 1):
        cell = sheet.cell(
            column=column,
            row=1,
            value=name
        )
        cell.font = Font(bold=True)
        cell.border = border
        cell.alignment = alignment

    counter = 1
    for index, value in enumerate(data, 2):
        for i in value.values():
            cell = sheet.cell(
                column=counter,
                row=index,
                value=str(i) if type(i) == list else i
            )
            cell.alignment = Alignment(horizontal='left')
            counter += 1

        counter = 1

    for i in 'ABCDEFGHI':
        sheet.column_dimensions[i].width = 30

    datetime_now = get_date_and_time()
    workbook.save(f"resulting files/{file_name} {datetime_now}.xlsx")


def main():

    # driver = uc.Chrome()
    # print("Получение списка всех ссылок из категории:")

    # urls = get_all_notebook_urls(driver)
    #
    # with open('urls.txt', 'w') as file:
    #     file.write('\n'.join(urls))
    #
    #     print("Получение характеристик всех игровых ноутбуков:")

    # with open('urls.txt', 'r') as file:
    #     urls = list(map(lambda line: line.strip(), file.readlines()))
    #     print(urls)
    #     info_dump = []
    #     for url in tqdm(urls, ncols=70, unit='notebook',
    #                     colour='green', file=sys.stdout):
    #         info_dump.append(parse_characteristics_page(driver, url))
    #
    #     for i in info_dump:
    #         print(i)

    # with open('notebooks_list_pickle.txt', 'wb+') as file:
    #     pickle.dump(info_dump, file)

    with open('notebooks_list_pickle.txt', 'rb') as file:
        info_dump = pickle.load(file)
        for i in info_dump:
            print(i)

    column_names = [
            "Категория",
            "Наименование",
            "Цена",
            "Доступность",
            "Ссылка на товар",
            "Описание",
            "Главное изображение",
            "Лист с картинками",
            "Характеристики",
    ]

    to_excel(info_dump, column_names, file_name="info_dump")


if __name__ == '__main__':
    main()