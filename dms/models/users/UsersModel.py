from dms import db
from typing import Dict, List


class UsersModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=False)
    email_address = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(10), nullable=False, unique=False)
    role_id = db.Column(
        db.Integer, db.ForeignKey("roles.id"), nullable=False, unique=False
    )
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False, unique=False
    )
    rights_id = db.Column(
        db.Integer, db.ForeignKey("rights.id"), nullable=False, unique=False
    )
    create_date = db.Column(db.DateTime, nullable=False, unique=False)
    update_date = db.Column(db.DateTime, nullable=True, unique=False)

    credentials = db.relationship("CredentialsModel", backref="user")

    def __init__(
        self,
        _id: int,
        name: str,
        email_address: str,
        password: str,
        role_id: int,
        project_id: int,
        rights_id: int,
        create_date,
        update_date,
    ):
        self.id = _id
        self.name = name
        self.email_address = email_address
        self.password = password
        self.role_id = role_id
        self.project_id = project_id
        self.rights_id = rights_id
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
