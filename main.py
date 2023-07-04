from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections
import argparse

YEAR_COMPANY_FOUNDATTION = 1920

def get_ending(year):
    
    num = year % 100
    if num > 4 and num < 21: 
        return 'лет'
    
    num = num % 10
    if num == 1: 
        return 'год'
    
    if num > 1 and num < 5: 
        return 'года'
    
    return 'лет'

def main():

    parser = argparse.ArgumentParser(
        description='Запускает сайт и заполняет раздел товаров информацией указанной в .xlsx файле'
    )
    parser.add_argument('file', help='Введите путь к .xlsx файлу с описанием товаров')
    args = parser.parse_args()

    group_wines = collections.defaultdict(list)
    pd = pandas.read_excel(args.file, na_values=None, keep_default_na=False)
    wines = pd.to_dict('index')

    lifetime = datetime.datetime.now().year - YEAR_COMPANY_FOUNDATTION

    for wine in wines:
        group_wines[wines[wine]['Категория']].append({'title': wines[wine]['Название'], 
                                                     'category': wines[wine]['Категория'],
                                                     'sort': wines[wine]['Сорт'],
                                                     'price': wines[wine]['Цена'],
                                                     'image': wines[wine]['Картинка'],
                                                     'offer': wines[wine]['Акция']})

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        age = lifetime,
        ending = get_ending(lifetime),
        group_wines = group_wines,
        
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
