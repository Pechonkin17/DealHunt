from flask import Flask, render_template, request
from db.mongo_client import get_games_collection

app = Flask(__name__)
collection = get_games_collection()


@app.route('/')
def index():
    games = list(collection.find())
    return render_template('index.html', games=games)


@app.route('/filtered')
def filtered_games():
    sort_order = request.args.get('sort', 'up')
    min_price = request.args.get('minPrice', type=float)
    max_price = request.args.get('maxPrice', type=float)
    search_title = request.args.get('searchTitle', '').lower()

    query = {}

    if min_price is not None:
        query['price'] = {'$gte': min_price}

    if max_price is not None:
        if 'price' in query:
            query['price']['$lte'] = max_price
        else:
            query['price'] = {'$lte': max_price}

    if search_title:
        query['title'] = {'$regex': search_title, '$options': 'i'}

    sort_dir = 1 if sort_order == 'up' else -1
    games = list(collection.find(query).sort('price', sort_dir))

    return render_template('index.html', games=games)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)
