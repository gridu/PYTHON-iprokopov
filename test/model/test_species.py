from app import app
from app.model.species import Species, db
import unittest
import uuid


class FlaskBookshelfTests(unittest.TestCase):

    def test_should_add_species(self):
        name = uuid.uuid4().hex
        description = uuid.uuid4().hex
        self.assertTrue(len([x for x in Species.get_all() if name in x]) == 0)
        Species.add(name, description, 100500)
        self.assertTrue(len([x for x in Species.get_all() if name in x]) == 1)
        species = Species.query.filter_by(name=name).filter_by(description=description).first()
        if species is not None:
            db.session.delete(species)
            db.session.commit()
