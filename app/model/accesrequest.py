from app import db
from datetime import datetime
import json
import logging


class AccessRequest(db.Model):
    __tablename__ = "access_requests"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    center_id = db.Column('center_id', db.Integer, db.ForeignKey('centers.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def add(_center_id):
        request = AccessRequest(center_id=_center_id)
        logging.info(f"Saving {request} to access_requests table")
        db.session.add(request)
        db.session.commit()

    @staticmethod
    def get_all():
        return [AccessRequest.json(request) for request in AccessRequest.query.all()]

    def json(self):
        return {
            'center_id': self.center_id,
            'timestamp': self.timestamp
        }

    def __str__(self):
        return f"{self.center_id} at {self.timestamp}"

    def __repr__(self):
        res = {
            'center_id': self.center_id,
            'timestamp': self.timestamp
        }
        return json.dumps(res)
