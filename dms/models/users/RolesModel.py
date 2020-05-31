from dms import db
from .UsersModel import UsersModel


class RolesModel(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(50), unique=True, nullable=False)
    create_date = db.Column(db.DateTime, unique=False, nullable=False)
    update_date = db.Column(db.DateTime, unique=False, nullable=True)

    users = db.relationship("UsersModel", backref="role")

    def __init__(
        self, _id: int, role_name: str, description: str, create_date, update_date
    ):
        self.id = _id
        self.role_name = role_name
        self.description = description
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_roles(cls):
        return cls.query.order_by(RolesModel.role_name).all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(role_name=name).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()

