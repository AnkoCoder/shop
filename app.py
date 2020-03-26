from flask import Flask, render_template, escape, request
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    products = relationship('Product', backref = 'category')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, ForeignKey=('category.id'))
    name = db.Column(db.String(80), unique=True, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    items = relationship('OrderItem', backref = 'product')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(80), unique=True, nullable=False)
    items = relationship('OrderItem', backref = 'order')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey=('order.id'))
    product_id = db.Column(db.Integer, ForeignKey=('product.id'))
    quantity = db.Column(db.Integer, nullable=False)

@app.route('/')
def catalog():
    catalog = Category.query.all()
    return render_template('products.html', catalog=catalog)
