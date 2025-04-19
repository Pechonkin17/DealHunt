from flask import Flask, render_template, request
from parser import parse_steam_discounts


app = Flask(__name__)


games = parse_steam_discounts()


@app.route('/filtered')
def filtered_games():
    global games
    # Параметри з запиту
    sort_order = request.args.get('sort', 'up')
    min_price = request.args.get('minPrice', type=float)
    max_price = request.args.get('maxPrice', type=float)
    search_title = request.args.get('searchTitle', '').lower()

    # Фільтрація
    filtered = games

    if min_price is not None and max_price is not None:
        filtered = [g for g in filtered if g['price'] >= min_price]
        if max_price > min_price:
            filtered = [g for g in filtered if g['price'] <= max_price]
        elif max_price <= min_price:
            filtered = [g for g in filtered if g['price'] == min_price]
        elif max_price >= 4000:
            filtered = [g for g in filtered if g['price'] <= 4000]
    elif min_price is not None and max_price is None:
        filtered = [g for g in filtered if g['price'] >= min_price]
    elif max_price is not None and min_price is None:
        filtered = [g for g in filtered if g['price'] <= max_price]


    if search_title:
        filtered = [g for g in filtered if search_title in g['title'].lower()]

    # Сортування
    reverse = sort_order == 'down'
    filtered = sorted(filtered, key=lambda g: g['price'], reverse=reverse)

    return render_template('index.html', games=filtered)


@app.route('/', methods=['GET'])
def index():
    global games
    return render_template('index.html', games=games)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)