from dms import db
from typing import Dict, List


class CredentialsModel(db.Model):
    __tablename__ = "credentials"

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False, unique=False)
    create_date = db.Column(db.DateTime, nullable=False, unique=False)
    update_date = db.Column(db.DateTime, nullable=True, unique=False)

    users = db.relationship("UsersModel", backref="credentials")

    def __init__(self, _id, email_address, password, create_date, update_date,):
        self._id = id
        self.email_address = email_address
        self.password = password
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_credential_by_email_address(cls, email_address):
        return cls.query.filter_by(email_address=email_address).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()