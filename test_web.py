import os
import tempfile

import pytest
from lxml import etree

from app import app, Category, Product


@pytest.fixture
def client():
    # db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    # app.config['TESTING'] = True

    with app.test_client() as client:
        # with flaskr.app.app_context():
        #     flaskr.init_db()
        yield client
    # os.close(db_fd)
    # os.unlink(flaskr.app.config['DATABASE'])


def test_about(client):
    response = client.get('/about/')
    response = response.data.decode("utf-8")
    assert 'Dear customers! Our online shop is made for easy and fast shopping.' in response


def test_services(client):
    response = client.get('/services/')
    response = response.data.decode("utf-8")
    assert 'Remember! To use our delivery service you need to remember your telegram id and your order id.' in response


def test_contact(client):
    response = client.get('/contact/')
    response = response.data.decode("utf-8")
    assert 'We are hiring!' in response


def test_home(client):
    response = client.get('/')
    response = response.data.decode("utf-8")
    html = etree.HTML(response)
    assert len(html.cssselect('a.list-group-item')) == len(Category.query.all())
    assert len(html.cssselect('div.col-lg-4')) == len(Product.query.all())


def test_category(client):
    response = client.get('/category/1/')
    response = response.data.decode("utf-8")
    html = etree.HTML(response)
    assert len(html.cssselect('div.col-lg-4')) == len(Category.query.get(1).products)
