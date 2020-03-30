from app import app
from app.model.animal import Animal
import unittest
import uuid


class FlaskBookshelfTests(unittest.TestCase):

    def test_should_not_add_animal(self):
        name = uuid.uuid4().hex
        description = uuid.uuid4().hex
        self.assertTrue(len([x for x in Animal.get_all() if name in x]) == 0)
        self.assertRaises(ValueError, Animal.add, -1, name, description, 5, -1, 100500)
        self.assertTrue(len([x for x in Animal.get_all() if name in x]) == 0)
