import os
import requests
from bs4 import BeautifulSoup
from typing import List
from models.game_info import GameInfo
from pymongo.collection import Collection


class SteamParser:
    def __init__(self, collection: Collection):
        self.collection = collection
        os.makedirs('./static/images/games', exist_ok=True)

    def fetch_discounts(self) -> List[GameInfo]:
        url = 'https://store.steampowered.com/search/?specials=1'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        games: List[GameInfo] = []

        for idx, game in enumerate(soup.select('.search_result_row')):
            title = game.select_one('.title').text.strip()
            link = game['href']

            try:
                discount_wrapper = game.select_one('.search_discount_and_price')
                discount_block = discount_wrapper.select_one('.discount_block')
                discount = discount_block.get('data-discount', 'No discount')
            except AttributeError:
                discount = "No discount"

            try:
                price_div = game.select_one('.search_price_discount_combined')
                price_str = price_div.get('data-price-final')
                price = float(price_str[:-2]) if price_str else 0.0
            except (AttributeError, ValueError):
                price = 0.0

            try:
                img_tag = game.select_one('img')
                img_url = img_tag['src']
                img_data = requests.get(img_url).content
                img_filename = f'./static/images/games/game_{idx + 1}.jpg'

                with open(img_filename, 'wb') as f:
                    f.write(img_data)
            except Exception:
                img_url = None
                img_filename = None

            game_info: GameInfo = {
                'title': title,
                'link': link,
                'discount': discount,
                'price': price,
                'image_url': img_url,
                'image_path': img_filename
            }

            games.append(game_info)

            if not self.collection.find_one({'title': title}):
                self.collection.insert_one(game_info)

        return games
