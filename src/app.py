"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
# pipenv run start
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

############################################################################ GET all Memebers

@app.route('/members', methods=['GET'])
def handle_hello():

    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

############################################################################ POST

@app.route('/member', methods=['POST'])
def add_member():
    body_last_name = request.json.get("last_name")
    body_first_name = request.json.get("first_name")
    body_age = request.json.get("age")
    body_id = request.json.get("id")
    body_lucky_numbers = request.json.get("lucky_numbers")
    member = {
        "id": body_id or jackson_family._generateId(),   #### valido id
        "first_name": body_first_name,
        "last_name": body_last_name,
        "age": body_age,
        "lucky_numbers": body_lucky_numbers,
    }
    jackson_family.add_member(member)
    return jsonify(None), 200

######################################################################### GET INT = ID
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_id(member_id):
    member = jackson_family.get_member(member_id)
    return jsonify(member), 200

# pipenv run test
########################################################################### DELETE

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member_id(member_id):
    member = jackson_family.delete_member(member_id)
    return jsonify({"done": True}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
