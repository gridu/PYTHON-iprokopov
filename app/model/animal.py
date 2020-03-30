from app import db
import app.model.species as spec
import logging

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'age': {'type': 'integer'},
        'species': {'type': 'integer'},
        'price': {'type': 'integer'}
    },
    'required': ['name', 'age', 'species']
}


class Animal(db.Model):
    __tablename__ = "animals"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    center_id = db.Column('center_id', db.Integer, db.ForeignKey('centers.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    age = db.Column(db.Integer, nullable=False)
    species = db.Column('species_id', db.Integer, db.ForeignKey('species.id'), nullable=False)
    price = db.Column(db.Integer, nullable=True)
    # animal = db.relationship('Species')

    def json(self):
        return {
            'id': self.id,
            'center_id': self.center_id,
            'name': self.name,
            'description': self.description,
            'age': self.age,
            'species': self.species,
            'price': self.price
        }

    def get_diff(self, _name, _description, _age, _species, _price):
        res = {}
        if self.name != _name:
            res["name"] = f"{self.name} -> {_name}"
        if self.description != _description:
            res["description"] = f"{self.description} -> {_description}"
        if self.age != _age:
            res["age"] = f"{self.age} -> {_age}"
        if self.species != _species:
            res["species"] = f"{self.species} -> {_species}"
        if self.price != _price:
            res["price"] = f"{self.price} -> {_price}"
        return str(res)

    @staticmethod
    def get_all():
        return [repr(animal) for animal in Animal.query.all()]

    @staticmethod
    def get_by_species(_species_id):
        return [repr(animal) for animal in Animal.query.filter_by(species=_species_id)]

    @staticmethod
    def get_by_id(_id):
        return Animal.json(Animal.query.filter_by(id=_id).first())

    @staticmethod
    def get_by_center_id(_id):
        return [repr(animal) for animal in Animal.query.filter_by(center_id=_id)]

    @staticmethod
    def add(_center_id, _name, _description, _age, _species, _price):
        try:
            spec.Species.get_by_id(_species)
            animal = Animal(center_id=_center_id, name=_name, description=_description, age=_age, species=_species,
                            price=_price)
            logging.info(f"Saving new animal {repr(animal)} to database")
            db.session.add(animal)
            db.session.commit()
        except AttributeError:
            message = f"Failed to save new animal to database due to incorrect species {_species} value"
            logging.warning(message)
            raise ValueError(message)

    @staticmethod
    def update(_id, _center_id, _name, _description, _age, _species, _price):
        animal = Animal.query.filter_by(id=_id).filter_by(center_id=_center_id).first()
        if animal is not None:
            diff = animal.get_diff(_name, _description, _age, _species, _price)
            logging.info(f"Updating animal with id {_id} with new values: {diff}")
            animal.name = _name
            animal.description = _description
            animal.age = _age
            animal.species = _species
            animal.price = _price
            db.session.add(animal)
            db.session.commit()
        else:
            message = f"Could not update animal due to incorrect id({_id}) or owner({_center_id})"
            logging.warning(message)
            raise ValueError(message)

    @staticmethod
    def delete(_id, _center_id):
        animal = Animal.query.filter_by(id=_id).filter_by(center_id=_center_id).first()
        if animal is not None:
            db.session.delete(animal)
            db.session.commit()
            logging.info(f"Animal with id {_id} was removed from database")
        else:
            message = f"Could not delete animal due to incorrect id({_id}) or owner({_center_id})"
            logging.warning(message)
            raise ValueError(message)

    def __repr__(self):
        return f"{self.name} - {self.id} - {self.species}"
