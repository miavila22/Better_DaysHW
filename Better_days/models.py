from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy #ORM (Object Relationa Mapper) remember this! 
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid #PK primary key
from flask_marshmallow import Marshmallow

from .helpers import get_image

#now we need to instantiate all our classes. Needs objects for database and login
db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow() 

@login_manager.user_loader
#function time for user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object

    """
    return User.query.get(user_id)

#Now a class for user that is ogin got to keep all information email, password, name, username, etc object=database object...
class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30)) #the interger is like VARCHAR remember that. 
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

#Now we INSERT INTO
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)

#Methods for attributes 
    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"


class Product(db.Model): 
    prod_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String)
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    #now the methods 

    def __init__(self, name, price, qty, image="", description=""):
        self.prod_id = self.set_id()
        self.name = name
        self.image = self.set_image(image, name)
        self.description = description
        self.price = price
        self.qty = qty 

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_image(self, image, name):
        print('image')
        if not image:
            print('We dont have an image')
            image = get_image(name)

        return image
    
    # Now we have to give the customers an option to adjust the quantity of the products

    def decrement_quantity(self, qty):
        self.qty -= int(qty)
        return self.qty
     
    def increment_quantity(self, qty):
        self.qty += int(qty)
        return self.qty
    
    def __repr__(self):
        return f"<Product: {self.name}>"
    



class Customer(db.Model):
    cust_id = db.Column(db.String, primary_key=True)
    date_created = db.Column(db.String, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'customer', lazy=True)

    def __init__(self, cust_id):
        self.cust_id = cust_id

    def __repr__(self):
        return f"<Customer: {self.cust_id}"
    

    

class ProdOrder(db.Model):
    prodorder_id = db.Column(db.String, primary_key=True)
    prod_id = db.Column(db.String, db.ForeignKey('product.prod_id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price= db.Column(db.Numeric(precision = 10, scale = 2), nullable=False)
    order_id = db.Column(db.String, db.ForeignKey('order.order_id'), nullable=False)
    cust_id = db.Column(db.String, db.ForeignKey('customer.cust_id'), nullable=False)

    def __init__(self, prod_id, qty, price, order_id, cust_id):
        self.prodorder_id = self.set_id()
        self.prod_id = prod_id 
        self.qty = qty
        self.price = self.set_price(qty, price)
        self.order_id = order_id
        self.cust_id = cust_id

    def set_id(self):
        return str(uuid.uuid4())


    def set_price(self, qty ,price):
        qty = int(qty)
        price = float(price)

        self.price = qty * price
        return self.price
    
    def update_quantity(self, qty):
        self.qty = int(qty)
        return self.qty
    

    
class Order(db.Model):
    order_id = db.Column(db.String, primary_key=True)
    order_total = db.Column(db.Numeric(precision = 10, scale = 2), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow())
    prodord = db.relationship('ProdOrder', backref = 'order', lazy=True)

    def __init__(self):
        self.order_id = self.set_id()
        self.order_total = 0.00

    def set_id(self):
        return str(uuid.uuid4())
    
    def increment_ordertotal(self, price):

        self.order_total = float(self.order_total)
        self.order_total += float(price)

        return self.order_total
    
    def decrement_ordertotal(self, price):

        self.order_total = float(self.order_total)
        self.order_total -= float(price)

        return self.order_total
    
    def __repr__(self):
        return f"<Order: {self.order_id}>"
    




class ProductSchema(ma.Schema):
    class Meta: fields = ['prod_id', 'name', 'image', 'description', 'price', 'qty']

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)