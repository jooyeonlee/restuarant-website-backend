from flask import Blueprint, json, jsonify, request
from app.models import db, Menu, Order, OrderItem

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/menus', methods=['GET'])
def menus():
    menus = {a.name: a.to_dict() for a in Menu.query.all()}
    return jsonify(menus)

@api.route('/menu/<int:id>', methods=['GET'])
def get_menu(id):
    try:
        menu = Menu.query.get(id).to_dict()
        return jsonify(menu)
    except:
        return jsonify(f"Menu ID: {id} does not exist in the database")

@api.route('/menu/category/<cate>', methods=['GET'])
def get_category(cate):
    try:
        menu = {a.name: a.to_dict() for a in Menu.query.filter_by(category=cate).all()}
        return jsonify(menu)
    except:
        return jsonify(f"Category: {cate} does not exist in the database")

@api.route('/addmenu', methods=['POST'])
def addmenu():
    req = request.get_json()
    newmenu = Menu()
    newmenu.from_dict(req)
    db.session.add(newmenu)
    db.session.commit()

    return jsonify({'Created': Menu.query.all()[-1].to_dict()})

@api.route('/menu/<int:id>', methods=['PUT'])
def updatemenu(id):
    resp = request.get_json()
    menu = Menu.query.get(id)
    menu.from_dict(resp)
    db.session.commit()
    return jsonify({'Updated': menu.to_dict()})

@api.route('/orders', methods=['GET'])
def orders():
    orders = {a.id: a.to_dict() for a in Order.query.all()}
    return jsonify(orders)

@api.route('/order/<int:id>', methods=['GET'])
def get_order(id):
    try:
        order = Order.query.get(id).to_dict()
        return jsonify(order)
    except:
        return jsonify(f"Order ID: {id} does not exist in the database")

@api.route('/order/user/<uid>', methods=['GET'])
def getorderbyuser(uid):
    try:
        order = {a.id: a.to_dict() for a in Order.query.filter_by(userid=uid).all()}
        return jsonify(order)
    except:
        return jsonify(f"UserID: {uid} does not have any order in the database")

@api.route('/addorder', methods=['POST'])
def addorder():
    req = request.get_json()
    neworder = Order()
    neworder.from_dict(req)
    db.session.add(neworder)
    db.session.commit()

    return jsonify({'Created': Order.query.all()[-1].to_dict()})

@api.route('/order/<int:id>', methods=['PUT'])
def updateorder(id):
    resp = request.get_json()
    order = Order.query.get(id)
    order.from_dict(resp)
    db.session.commit()
    return jsonify({'Updated': order.to_dict()})

@api.route('/orderitems', methods=['GET'])
def orderitems():
    items = {a.id: a.to_dict() for a in OrderItem.query.all()}
    return jsonify(items)

@api.route('/orderitem/<int:id>', methods=['GET'])
def get_orderitem(id):
    try:
        item = OrderItem.query.get(id).to_dict()
        return jsonify(item)
    except:
        return jsonify(f"Order Item ID: {id} does not exist in the database")

@api.route('/orderitem/order/<int:id>', methods=['GET'])
def getorderitemsfororder(id):
    try:
        item = {a.id: a.to_dict() for a in OrderItem.query.filter_by(orderid=id).all()}
        return jsonify(item)
    except:
        return jsonify(f"Order ID: {id} does not have any order items in the database")

@api.route('/orderitem/menu/<int:id>', methods=['GET'])
def getorderitembymenu(id):
    try:
        item = {a.id: a.to_dict() for a in OrderItem.query.filter_by(menuid=id).all()}
        return jsonify(item)
    except:
        return jsonify(f"Menu ID: {id} does not have any order items in the database")

@api.route('/addorderitem', methods=['POST'])
def addorderitem():
    req = request.get_json()
    newitem = OrderItem()
    newitem.from_dict(req)
    db.session.add(newitem)
    db.session.commit()

    return jsonify({'Created': OrderItem.query.all()[-1].to_dict()})

@api.route('/orderitem/<int:id>', methods=['PUT'])
def updateorderitem(id):
    resp = request.get_json()
    item = OrderItem.query.get(id)
    item.from_dict(resp)
    db.session.commit()
    return jsonify({'Updated': item.to_dict()})

@api.route('/orderitemmenu/<int:id>', methods=['GET'])
def get_menu_orderitem(id):
    try:
        items = [a.to_dict() for a in OrderItem.query.filter_by(orderid=id).all()]
        menuitem_dict = {}
        for item in items:
            menu_id = item['menuid']
            menu = Menu.query.get(menu_id)
            print(menu.to_dict())
            temp = {'item': menu.to_dict(), 'quantity': item['quantity'], 'price': item['price']}
            print(temp)
            menuitem_dict[menu_id] = temp
            print(menuitem_dict)
        return jsonify(menuitem_dict)
    except:
        return jsonify("Order ID: {id} does not have any order items in the database")
