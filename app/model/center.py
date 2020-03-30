from app import db
from app.model.animal import Animal
import logging

schema = {
    'type': 'object',
    'properties': {
        'login': {'type': 'string'},
        'password': {'type': 'string'},
        'address': {'type': 'string'},
    },
    'required': ['login', 'password', 'address']
}


class Center(db.Model):
    __tablename__ = "centers"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)

    @staticmethod
    def add(_login, _password, _address):
        center = Center(login=_login, password=_password, address=_address)
        db.session.add(center)
        db.session.commit()
        logging.info(f"New center with login {_login} was added to database")

    @staticmethod
    def get_all():
        return [repr(center) for center in Center.query.all()]

    @staticmethod
    def get_by_login(_login):
        return Center.query.filter_by(login=_login).first()

    @staticmethod
    def get_by_id(_id):
        return Center.json(Center.query.filter_by(id=_id).first())

    @staticmethod
    def remove(_id):
        center = Center.query.filter_by(id=_id).first()
        if center is not None:
            db.session.delete(center)
            db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'login': self.login,
            'address': self.address,
            'password': self.password,
            'animals': Animal.get_by_center_id(self.id)
        }

    @staticmethod
    def login_password_match(_login, _password):
        center = Center.query.filter_by(login=_login).filter_by(password=_password).first()
        if center is None:
            return False
        else:
            return True

    def __str__(self):
        return f"{self.login} is from {self.address}"

    def __repr__(self):
        return f"{self.login} - {self.id}"
