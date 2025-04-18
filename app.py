from flask import Flask, render_template
from parser import parse_steam_discounts


app = Flask(__name__)


games = parse_steam_discounts()


@app.route('/by_price')
def sorted_games_by_price():
    global games
    sorted_games = sorted(games, key=lambda game: game['price'])
    print(sorted_games)
    return render_template('index.html', games=sorted_games)


@app.route('/', methods=['GET'])
def index():
    global games
    return render_template('index.html', games=games)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)