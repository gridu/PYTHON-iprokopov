from app import db
import app.model.animal as animal
import logging

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description': {'type': 'string'},
        'price': {'type': 'integer'}
    },
    'required': ['name', 'description', 'price']
}


class Species(db.Model):
    __tablename__ = "species"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    # animals = db.relationship('Animal', lazy='dynamic', back_populates='animal')

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'approx_price': self.price,
            'animals': animal.Animal.get_by_species(self.id)
        }

    @staticmethod
    def add(_name, _description, _price):
        species = Species(name=_name, description=_description, price=_price)
        db.session.add(species)
        db.session.commit()
        logging.info(f"New species with name {_name} was added to database")

    @staticmethod
    def delete(_id):
        species = Species.query.filter_by(id=_id).first()
        if species is not None:
            db.session.delete(species)
            db.session.commit()

    @staticmethod
    def get_by_id(_id):
        return Species.json(Species.query.filter_by(id=_id).first())

    @staticmethod
    def get_all():
        return [repr(animal) for animal in Species.query.all()]

    def __repr__(self):
        return f"{self.name} - {len(animal.Animal.get_by_species(self.id))}"