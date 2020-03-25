from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def products_list():
    with open('db.json') as f:
        products = json.load(f)
    return render_template('products.html', catalog=products)
