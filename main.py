from bs4 import BeautifulSoup
import requests

page = requests.get('https://www.otomoto.pl/motocykle-i-quady/yamaha/mt/?search%5Bfilter_float_engine_capacity%3Ato%5' +
                    'D=125&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_features%5D%5B0%5D=abs&search%5Bfil' +
                    'ter_enum_no_accident%5D=1&search%5Bprivate_business%5D=private&search%5Bcountry%5D=')

soup = BeautifulSoup(page.text, 'html.parser')

offers_list = soup.find_all('article')

for article in offers_list:
    print(article['data-ad-id'])