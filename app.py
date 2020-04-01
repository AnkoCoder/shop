from flask import Flask, render_template
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'something'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
admin = Admin(app, name='products')
db = SQLAlchemy(app)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    products = db.relationship('Product', backref='category')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(80), unique=True, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    items = db.relationship('OrderItem', backref='product')


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.String(80), nullable=False)
    items = db.relationship('OrderItem', backref='order')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)


admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(OrderItem, db.session))


@app.route('/')
def catalog():
    categories = Category.query.all()
    return render_template('products.html', categories=categories)
