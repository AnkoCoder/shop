from app import db, Category, Product

db.drop_all()
db.create_all()

categories = []
categories.append(Category(name='Clothes'))
categories.append(Category(name='Underwear'))
categories.append(Category(name='Footwear'))


products = []
products.append(Product(name='Short dress', cost=50, category_id=1))
products.append(Product(name='Long dress', cost=70, category_id=1))
products.append(Product(name='Jeans', cost=50, category_id=1))
products.append(Product(name='T-shirt', cost=20, category_id=1))
products.append(Product(name='Pants', cost=50, category_id=1))
products.append(Product(name='Skirt', cost=45, category_id=1))
products.append(Product(name='Coat', cost=100, category_id=1))
products.append(Product(name='Scarf', cost=15, category_id=1))
products.append(Product(name='Pullover', cost=50, category_id=1))
products.append(Product(name='Blouse', cost=40, category_id=1))
products.append(Product(name='Shirt', cost=50, category_id=1))
products.append(Product(name='Tights', cost=30, category_id=2))
products.append(Product(name='Bra', cost=90, category_id=2))
products.append(Product(name='Underpants', cost=40, category_id=2))
products.append(Product(name='String underpants', cost=40, category_id=2))
products.append(Product(name='Tanga  underpants', cost=40, category_id=2))
products.append(Product(name='Bikini underpants', cost=40, category_id=2))
products.append(Product(name='Slingbacks', cost=40, category_id=3))
products.append(Product(name='Flats', cost=50, category_id=3))
products.append(Product(name='Stiletto', cost=60, category_id=3))
products.append(Product(name='Sandals', cost=30, category_id=3))
products.append(Product(name='Flip-Flops', cost=20, category_id=3))
products.append(Product(name='Sneakers', cost=80, category_id=3))
products.append(Product(name='Boots', cost=90, category_id=3))
        
for category in categories:
    db.session.add(category)

for product in products:
    db.session.add(product)


db.session.commit()
