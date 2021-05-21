import re
from flask import Blueprint, request, jsonify
from vinyl_inventory.helpers import token_required
from vinyl_inventory.models import User, Vinyl, vinyl_schema,vinyl_schemas, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 73}

#CREATE VINYL ENDPOINT
@api.route('/vinyls', methods = ['POST'])
@token_required
def create_drone(current_user_token): #coming form token_required decorator
    name = request.json['name']
    label = request.json['label']
    format = request.json['format']
    country = request.json['country']
    released = request.json['released']
    genre = request.json['genre']
    style = request.json['style']
    price = request.json['price']
    user_token = current_user_token.token

    
    vinyls = Vinyl(name, label, format, country, released, genre, style, price, user_token, id = '')

    db.session.add(vinyls)
    db.session.commit()

    response = vinyl_schema.dump(vinyls)
    return jsonify(response)

#RETRIEVE ALL VINYLS
@api.route('/vinyls', methods = ['GET'])
@token_required
def get_vinyls(current_user_token):
    owner = current_user_token.token
    vinyls = Vinyl.query.filter_by(user_token = owner).all()
    response = vinyl_schemas.dump(vinyls)
    return jsonify(response)

#RETRIEVE ONE VINYL ENDPOINT
@api.route('/vinyls/<id>', methods = ['GET'])
@token_required
def get_vinyl(current_user_token, id):
    vinyl = Vinyl.query.get(id)
    response = vinyl_schema.dump(vinyl)
    return jsonify(response)

@api.route('/vinylss/<id>', methods = ['POST', 'PUT'])
@token_required
def update_vinyl(current_user_token, id):
    vinyl = Vinyl.query.get(id)

    vinyl.name = request.json['name']
    vinyl.label = request.json['label']
    vinyl.format = request.json['format']
    vinyl.country = request.json['country']
    vinyl.released = request.json['released']
    vinyl.genre = request.json['genre']
    vinyl.style = request.json['style']
    vinyl.price = request.json['price']
    vinyl.user_token = current_user_token.token
    print(vinyl.name)
    db.session.commit()
    response = vinyl_schema.dump(vinyl)
    return jsonify(response)

#DELETE DRONE BY ID
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_vinyl(current_user_token, id):
    vinyl = Vinyl.query.get(id)
    if vinyl:
        db.session.delete(vinyl)
        db.session.commit()

        response = vinyl_schema.dump(vinyl)
        return jsonify(response)
    else:
        return jsonify({'Error': 'This vinyl does not exist'})