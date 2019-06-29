from bs4 import BeautifulSoup
import requests
from flask import Flask, g, jsonify
import sqlite3


DATABASE = 'MT125_storage.db'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return 'hello'


@app.route('/create_table')
def create_table():
    cursor = get_db().cursor()
    cursor.execute('CREATE TABLE offers(article_id int, article_price int, article_year int, article_mileage int, '
                   + 'article_link message_text )').fetchall()
    cursor.close()
    return 'Done'


@app.route('/printall')
def printall():
    cursor = get_db().cursor()
    data = cursor.execute('SELECT * FROM offers').fetchall()
    cursor.close()
    return jsonify(data)


def scrap_the_data():
    """Function that scrap desired data and returns list of records as dictionaries"""

    # creating list that will contain data of our offers
    turbolist = []

    page = requests.get(
        'https://www.otomoto.pl/motocykle-i-quady/yamaha/mt/?search%5Bfilter_float_engine_capacity%3Ato%5' +
        'D=125&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_features%5D%5B0%5D=abs&search%5Bfil' +
        'ter_enum_no_accident%5D=1&search%5Bprivate_business%5D=private&search%5Bcountry%5D=')

    soup = BeautifulSoup(page.text, 'html.parser')

    # creating list of offers with parsing by 'article' tag
    offers_list = soup.find_all('article')

    # loop adding dict to data
    for article in offers_list:
        article_id = article['data-ad-id']
        article_price = article.find(class_='offer-price__number').contents[0].replace(' ', '')
        article_year = article.find_all(class_='offer-item__params-item')[0].span.contents[0]
        article_mileage = article.find_all(class_='offer-item__params-item')[1].span.contents[0]
        article_link = article['data-href']
        # checking if our record isn't already in database
        if not any(d['id'] == article_id for d in turbolist):
            turbolist.append(
                {'id': article_id, 'price': article_price, 'year': article_year, 'mileage': article_mileage,
                 'link': article_link})
    return turbolist


def correctly_message_variable(number):
    """ Function required to return grammatically correct messages about number of offers"""
    if number == 0:
        return '0 offers were'
    elif number == 1:
        return '1 offer was'
    elif number >= 2:
        return f'{number} offers were'


@app.route('/add_scrapped_data')
def add_data():

    cursor = get_db().cursor()
    articles_already_in_db = 0
    artcles_added_to_db = 0

    for single_offer in scrap_the_data():

        data = cursor.execute('SELECT article_id FROM offers WHERE article_id = ?', (single_offer['id'],)).fetchall()

        if data == 0:
            cursor.execute('INSERT INTO offers (article_id, article_price, article_year, article_mileage, article_link)'
                           'VALUES (?,?,?,?,?)', (list(single_offer.values())), ).fetchall()
            artcles_added_to_db += 1
            get_db().commit()
        else:
            articles_already_in_db += 1

    cursor.close()

    return f'{correctly_message_variable(artcles_added_to_db)} added to Database. ' \
        f'{correctly_message_variable(articles_already_in_db)} already there'


if __name__ == '__main__':
    app.run()
