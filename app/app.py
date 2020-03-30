from flask_jwt import JWT, jwt_required, current_identity
from flask import jsonify, request, Response
from app import app
from app.model.center import Center, schema as center_schema
from app.model.accesrequest import AccessRequest
from app.model.animal import Animal, schema as animal_schema
from app.model.species import Species, schema as species_schema
import logging
from flask_expects_json import expects_json


def authenticate(login, password):
    """
    Authentication method used by flask_jwt library

    Parameters:
    login (string): center's login
    password (string): center's password

    """
    logging.info("Trying to authenticate")
    if Center.login_password_match(login, password):
        logging.info("Login and password are correct")
        center = Center.get_by_login(login)
        AccessRequest.add(center.id)
        return center


def identity(payload):
    """
        Identity method used by flask_jwt library.

        Parameters:
        login (string): center's login
        password (string): center's password

        """
    center_id = payload['identity']
    return Center.get_by_id(center_id)


jwt = JWT(app, authenticate, identity)


@app.route('/animals')
def get_all_animals():
    logging.info("Get all animals route was triggered")
    return jsonify(Animal.get_all())


@app.route('/animals/<int:animal_id>')
def get_animal_by_id(animal_id):
    logging.info(f"Get animal with id {animal_id} route was triggered")
    return jsonify(Animal.get_by_id(animal_id))


@app.route('/animals/<int:animal_id>', methods=['PUT'])
@jwt_required()
def update_animal(animal_id):
    content = request.json
    current_user = current_identity
    logging.info(f"Update animal with id {animal_id} PUT route was triggered by user with id {current_user['id']}")
    try:
        Animal.update(animal_id, current_user["id"], content["name"], content["description"],
                      content["age"], content["species"], content["price"])

        return Response(status=201)
    except ValueError as error:
        return Response(str(error), status=400)


@app.route('/animals/<int:animal_id>', methods=['DELETE'])
@jwt_required()
def delete_animal(animal_id):
    current_user = current_identity
    logging.info(f"Delete animal with id {animal_id} DELETE route was triggered by user with id {current_user['id']}")
    try:
        Animal.delete(animal_id, current_user["id"])
        return Response(status=201)
    except ValueError as error:
        return Response(str(error), status=400)


@app.route('/centers')
def get_all_centers():
    logging.info(f"Get all centers GET route was triggered")
    return jsonify(Center.get_all())


@app.route('/species')
def get_all_species():
    logging.info(f"Get all centers GET route was triggered")
    return jsonify(Species.get_all())


@app.route('/species/<int:species_id>')
def get_species_by_id(species_id):
    logging.info(f"Get spices with id {species_id} GET route was triggered")
    return jsonify(Species.get_by_id(species_id))


@app.route('/centers/<int:center_id>')
def get_center_by_id(center_id):
    logging.info(f"Get center with id {center_id} GET route was triggered")
    return jsonify(Center.get_by_id(center_id))


@app.route("/register", methods=['POST'])
@expects_json(center_schema)
def register():
    content = request.json
    logging.info(f"Create new user with login {content['login']} POST route was triggered")
    Center.add(content["login"], content["password"], content["address"])
    return Response(status=201)


@app.route("/species", methods=['POST'])
@expects_json(species_schema)
@jwt_required()
def create_species():
    content = request.json
    current_user = current_identity
    logging.info(
        f"Create new species with name {content['name']} POST route was triggered by user with id {current_user['id']}")
    Species.add(content["name"], content["description"], content["price"])
    return Response(status=201)


@app.route("/animals", methods=['POST'])
@expects_json(animal_schema)
@jwt_required()
def create_animal():
    content = request.json
    current_user = current_identity
    logging.info(
        f"Create animal with name {content['name']} POST route was triggered by user with id {current_user['id']}")
    try:
        Animal.add(current_user["id"], content["name"], content.get("description", None),
                   content["age"], content["species"], content.get("price", None))
        return Response(status=201)
    except ValueError as error:
        return Response(str(error), status=400)
