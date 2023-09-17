import pickle
import re
import sys
from pprint import pprint
from random import randint
from time import sleep as pause
from time import time

from bs4 import BeautifulSoup
import undetected_chromedriver as uc

driver = uc.Chrome()

url = 'https://www.dns-shop.ru/catalog/17a89bb916404e77/platy-rasshireniya/'
url2 = 'https://www.dns-shop.ru/product/7b067fcc811b3361/susilka-dla-bela-na-radiator-podvesnaa-nika-sb5-65/characteristics/'

url3 = 'https://www.dns-shop.ru/product/ea019326cc42ed20/18-noutbuk-razer-blade-18-cernyj/characteristics/'
url4 = 'https://www.dns-shop.ru/product/c42c96d3b3b6ed20/susilka-dla-bela-podvesnaa-master-house-suskoritel/characteristics/'
url5 = 'https://www.dns-shop.ru/product/529f5ab4897998dc/mikrofon-aceline-amic-4-cernyj/characteristics/'

driver.get(url=url5)


pause(randint(9, 10))

soup = BeautifulSoup(driver.page_source, 'lxml')

print(soup.prettify())


name = soup.find('div', class_="product-card-description__title")
price = soup.find('div', class_="product-buy__price")
desc = soup.find('div', class_="product-card-description-text")
avail = soup.find('a', class_="order-avail-wrap__link ui-link ui-link_blue")
charcs = soup.find_all('div', class_="product-characteristics__spec-title")
cvalue = soup.find_all('div', class_="product-characteristics__spec-value")
main_picture = soup.find('img', class_="product-images-slider__main-img")
pictures_soup = soup.find_all('img', class_="product-images-slider__img loaded tns-complete")



# pictures_list = []
# for i in pictures_soup:
#     pictures_list.append(i.get('data-src'))



span_tags = soup.find_all('span')
for i in span_tags:
    if bool(str(i).find('data-go-back-catalog') != -1):
        category = i

tech_spec = {}
for f1, f2 in zip(charcs, cvalue):
    tech_spec[f1.text.rstrip().lstrip()] = f2.text.rstrip().lstrip()

# notebook = {}
#
# notebook["Категория"] = category.text.lstrip(': ')
# notebook["Наименование"] = name.text[15:]
# notebook["Цена"] = int(price.text.replace(' ', '')[:-1])
# notebook["Доступность"] = avail.text if avail is not None else 'Товара нет в наличии'
# notebook["Ссылка на товар"] = url3
# notebook["Описание"] = desc.text
# notebook["Главное изображение"] = main_picture.get('src')
# notebook["Лист с картинками"] = pictures_list

# notebook["Характеристики"] = list(tech_spec.items())
# for i, j in notebook.items():
#     print(i, j)

driver.close()
