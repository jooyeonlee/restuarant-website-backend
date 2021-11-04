from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from secrets import token_hex
import uuid


#db
db = SQLAlchemy()

class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(7,2), nullable=False)
    description = db.Column(db.String(1000), nullable=True, default='')
    category = db.Column(db.String(300), nullable=False)
    subcategory = db.Column(db.String(300), nullable=True, default='')
    image = db.Column(db.String(1000), nullable=True, default='')
    orderitem = relationship("OrderItem", back_populates="menu")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'image': self.image
        }

    def from_dict(self, new):
        if new.get('id'):
            self.id = new.get('id')
        if new.get('name'):
            self.name = new.get('name')
        if new.get('price'):
            self.price = new.get('price')
        if new.get('description'):
            self.description = new.get('description')
        if new.get('category'):
            self.category = new.get('category')
        if new.get('subcategory'):
            self.subcategory = new.get('subcategory')
        if new.get('image'):
            self.image = new.get('image')

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.String, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order = relationship("Order", back_populates="customer")

    def __init__(self, firstname, lastname, email, password, contact):
        self.id = str(uuid.uuid4())
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.contact = contact
        self.password = generate_password_hash(password)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'password': self.password,
            'datecreated': self.date_created
        }

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String, db.ForeignKey('customer.id'))
    status_id = db.Column(db.Integer, nullable = True, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_id = db.Column(db.String(100), nullable=True)
    coupon_id = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Numeric(9,2), nullable=False)
    customer = relationship("Customer", back_populates="order")
    orderitem = relationship("OrderItem", back_populates="order")

    def to_dict(self):
        return {
            'id': self.id,
            'userid' : self.userid,
            'status_id' : self.status_id,
            'date_created' : self.date_created,
            'payment_id' : self.payment_id,
            'coupon_id' : self.coupon_id,
            'price' : self.price
        }

class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    id = db.Column(db.Integer, primary_key=True)
    orderid = db.Column(db.Integer, db.ForeignKey('order.id'))
    menuid = db.Column(db.Integer, db.ForeignKey('menu.id'))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Numeric(9,2), nullable=False)
    order = relationship("Order", back_populates="orderitem")
    menu = relationship("Menu", back_populates="orderitem")

    def to_dict(self):
        return {
            'id': self.id,
            'orderid': self.orderid,
            'menuid' : self.menuid,
            'quantity' : self.quantity,
            'price' : self.price
        }
    