from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime

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

class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(30), nullable=False)
    status_id = db.Column(db.Integer, nullable = True, default=0)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_id = db.Column(db.String(100), nullable=True)
    coupon_id = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Numeric(9,2), nullable=False)
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

    def from_dict(self, new):
        if new.get('id'):
            self.id = new.get('id')
        if new.get('userid'):
            self.userid = new.get('userid')
        if new.get('status_id'):
            self.status_id = new.get('status_id')
        if new.get('payment_id'):
            self.payment_id = new.get('payment_id')
        if new.get('coupon_id'):
            self.coupon_id = new.get('coupon_id')
        if new.get('price'):
            self.price = new.get('price')

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
    
    def from_dict(self, new):
        if new.get('id'):
            self.id = new.get('id')
        if new.get('orderid'):
            self.orderid = new.get('orderid')
        if new.get('menuid'):
            self.menuid = new.get('menuid')
        if new.get('quantity'):
            self.quantity = new.get('quantity')
        if new.get('price'):
            self.price = new.get('price')