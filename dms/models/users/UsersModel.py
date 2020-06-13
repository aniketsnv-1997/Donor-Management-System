from datetime import datetime as dt

from dms import db
from typing import Dict, List


class UsersModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=False)
    email_address = db.Column(db.String(30), nullable=False, unique=True)
    role_id = db.Column(
        db.Integer, db.ForeignKey("roles.id"), nullable=False, unique=False
    )
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False, unique=False
    )
    rights_id = db.Column(
        db.Integer, db.ForeignKey("rights.id"), nullable=False, unique=False
    )

    credential_id = db.Column(
        db.Integer, db.ForeignKey("credentials.id"), nullable=False, unique=True
    )

    create_date = db.Column(db.DateTime, nullable=False, unique=False, default=dt.now())
    update_date = db.Column(db.DateTime, nullable=True, unique=False, default=dt.now())

    def __init__(self, _id, name, email_address, role_id, project_id, rights_id, credential_id, create_date, update_date,):
        self._id = id
        self.name = name
        self.email_address = email_address
        self.role_id = role_id
        self.project_id = project_id
        self.rights_id = rights_id
        self.credential_id = credential_id
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def find_by_email_address(cls, email_address: str):
        return cls.query.filter_by(email_address=email_address).first()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    # @classmethod
    # def commit_to_database(cls) -> None:
    #     db.session.commit()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
