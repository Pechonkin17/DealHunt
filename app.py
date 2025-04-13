from flask import Flask, render_template
from parser import parse_steam_discounts
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    games = parse_steam_discounts()
    return render_template('index.html', games=games)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999)
