from flask import Blueprint, json, jsonify, request
from app.models import db, Menu, Customer, Order, OrderItem

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