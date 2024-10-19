import requests
from bs4 import BeautifulSoup
import json
import unicodedata

def scrape(link: str):
    r = requests.get(link)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.content, 'html.parser')

    page = dict()

    # Extract title
    page['title'] = soup.find('h1', {'class': 'article-heading type--lion'}).text

    # Extract description
    page['description'] = soup.find('p', {'class': 'article-subheading type--dog'}).text

    # Extract ingredients
    page['ingredients'] = list()
    ingredients_list = soup.find('ul', {'class': 'mm-recipes-structured-ingredients__list'})
    for ingredient_list_item in ingredients_list.find_all('li'):
        ingredient = {'quantity': None, 'unit': None, 'name': None}
        for span in ingredient_list_item.find_all('span'):
            if 'data-ingredient-quantity' in span.attrs and span.text:
                ingredient['quantity'] = float('0' + span.text[:-1]) + unicodedata.numeric(span.text[-1])
            elif 'data-ingredient-unit' in span.attrs and span.text:
                ingredient['unit'] = span.text
            elif 'data-ingredient-name' in span.attrs and span.text:
                ingredient['name'] = span.text
        page['ingredients'].append(ingredient)

    return page

if __name__ == '__main__':
    links = ['https://www.allrecipes.com/recipe/214760/roasted-pecan-banana-bread-loaves/']
    for link in links:
        page = scrape(link)
        print(json.dumps(page, indent=2))
