from bs4 import BeautifulSoup
import requests

# creating list that will contain data of our offers
turbolist = []

page = requests.get('https://www.otomoto.pl/motocykle-i-quady/yamaha/mt/?search%5Bfilter_float_engine_capacity%3Ato%5' +
                    'D=125&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_features%5D%5B0%5D=abs&search%5Bfil' +
                    'ter_enum_no_accident%5D=1&search%5Bprivate_business%5D=private&search%5Bcountry%5D=')

soup = BeautifulSoup(page.text, 'html.parser')

# creating list of offers with parsing by 'article' tag
offers_list = soup.find_all('article')

# loop adding to data dict of
for article in offers_list:
    article_id = article['data-ad-id']
    # checking if our record isn't already in database
    if not any(d['id'] == article_id for d in turbolist):
        turbolist.append({'id': article_id, 'price': article.find(class_='offer-price__number').contents[0].replace(
            ' ', '')})


print(turbolist)
