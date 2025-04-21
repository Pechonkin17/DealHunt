import os
import requests
from bs4 import BeautifulSoup
from typing import List, TypedDict


class GameInfo(TypedDict):
    title: str
    link: str
    discount: str
    price: float
    image_url: str
    image_path: str


def parse_steam_discounts() -> List[GameInfo]:
    url = 'https://store.steampowered.com/search/?specials=1'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    games = []
    os.makedirs('./static/images/games', exist_ok=True)
    for idx, game in enumerate(soup.select('.search_result_row')):
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

        try:
            img_tag = game.select_one('img')
            img_url = img_tag['src']
            img_data = requests.get(img_url).content
            img_filename = f'./static/images/games/game_{idx + 1}.jpg'

            with open(img_filename, 'wb') as f:
                f.write(img_data)
        except Exception as e:
            img_url = None
            img_filename = None

        games.append({
            'title': title,
            'link': link,
            'discount': discount,
            'price': float(price[:-2]),
            'image_url': img_url,
            'image_path': img_filename
        })
    return games