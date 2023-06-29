from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections

def ending(year):
    
    num = year % 100
    if num > 4 and num < 21: return 'лет'
    
    num = num % 10
    if num == 1: return 'год'
    
    if num > 1 and num < 5: return 'года'
    
    return 'лет'

def main():

    group_wines = collections.defaultdict(list)
    pd = pandas.read_excel('wine3.xlsx', index_col=None, na_values=None, keep_default_na=False)
    wines = pd.to_dict('index')

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
        age = datetime.datetime.now().year - 1920,
        ending = ending(datetime.datetime.now().year - 1920),
        group_wines = group_wines,
        
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
