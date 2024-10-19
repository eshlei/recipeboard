import requests
from bs4 import BeautifulSoup
import json
import unicodedata

def scrape(link: str):
    # Get page source html
    r = requests.get(link)
    if r.status_code != 200:
        return None
    soup = BeautifulSoup(r.content, 'html.parser')

    page = dict()

    # Extract title
    page['title'] = soup.find('h1', {'class': 'article-heading type--lion'}).text

    # Extract description
    page['description'] = soup.find('p', {'class': 'article-subheading type--dog'}).text

    # Extract preview
    page['overview'] = {'prep-time': None, 'cook-time': None, 'additional-time': None, 'total-time': None, 'servings': None, 'yield': None}
    overview_list = soup.find('div', {'class': 'mm-recipes-details__content'})
    for overview_list_item in overview_list.find_all('div', {'class': 'mm-recipes-details__item'}):
        key_div, value_div = overview_list_item.find_all('div')
        key = key_div.text.replace(' ', '-').replace(':', '').lower()
        value = value_div.text
        page['overview'][key] = value

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

    # Extract directions
    page['directions'] = list()
    directions_list = soup.find('ol', {'id': 'mntl-sc-block_1-0'})
    for directions_list_items in directions_list.find_all('li'):
        for p in directions_list_items.find_all('p'):
            page['directions'].append(p.text[1:-1])

    # Extract nutrition-facts
    page['nutrition-facts'] = {'calories': None, 'fat': None, 'carbs': None, 'protein': None}
    nutrition_facts_table = soup.find('table', {'class': 'mm-recipes-nutrition-facts-summary__table'})
    for nutrition_facts_tr in nutrition_facts_table.find_all('tr'):
        value_div, key_div = nutrition_facts_tr.find_all('td')
        value = float(value_div.text.replace(' ', '').replace('g', ''))
        key = key_div.text.lower()
        page['nutrition-facts'][key] = value

    return page

if __name__ == '__main__':
    links = ['https://www.allrecipes.com/recipe/245027/creamy-pumpkin-pasta-bake/', 
             'https://www.allrecipes.com/recipe/214760/roasted-pecan-banana-bread-loaves/'
            ]
    for link in links:
        page = scrape(link)
        print(json.dumps(page, indent=2))
