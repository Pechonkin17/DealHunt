import requests
from bs4 import BeautifulSoup


def parse_steam_discounts():
    url = 'https://store.steampowered.com/search/?specials=1'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    games = []
    for game in soup.select('.search_result_row'):
        title = game.select_one('.title').text
        link = game['href']

        try:
            discount_wrapper = game.select_one('.search_discount_and_price')
            discount_block = discount_wrapper.select_one('.discount_block')
            discount = discount_block.get('data-discount', 'No discount')
        except AttributeError:
            discount = "No discount"

        try:
            price_div = game.select_one('.search_price_discount_combined')
            price = price_div.get('data-price-final')
        except AttributeError:
            price = "Unknown"

        games.append({
            'title': title,
            'link': link,
            'discount': discount,
            'price': float(price[:-2])
        })
    return games