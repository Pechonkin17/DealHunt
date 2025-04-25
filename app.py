from flask import Flask, render_template, request, make_response, redirect, url_for
from db.mongo_client import get_games_collection
import json
from bson import ObjectId


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


@app.route('/save_game/<game_id>')
def save_game(game_id):
    resp = make_response(redirect(url_for('index')))
    saved_games = request.cookies.get('saved_games')

    if saved_games:
        saved_games = json.loads(saved_games)
    else:
        saved_games = []

    if game_id not in saved_games:
        saved_games.append(game_id)

    resp.set_cookie('saved_games', json.dumps(saved_games))
    return resp


@app.route('/saved')
def saved():
    saved_games = request.cookies.get('saved_games')

    if saved_games:
        saved_game_ids = json.loads(saved_games)
        games = list(collection.find({'_id': {'$in': [ObjectId(id_) for id_ in saved_game_ids]}}))
    else:
        games = []

    return render_template('saved.html', games=games)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)
