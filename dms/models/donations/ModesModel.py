from dms.app import db
from .DonationsModel import DonationsModel


class MM(db.Model):
    __tablename__ = "modes_of_donation"

    id = db.Column(db.Integer, primary_key=True)
    mode_name = db.Column(db.String(15), unique=True, nullable=False)
    create_date = db.Column(db.DateTime, nullable=True, unique=False)
    update_date = db.Column(db.DateTime, nullable=True, unique=False)

    donations = db.relationship("DonationsModel", backref="mode", lazy=True)

    def __init__(self, _id: int, mode_name: str, create_date, update_date):
        self.id = _id
        self.mode_name = mode_name
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_modes(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name: str):
        return cls.query.filter_by(mode_name=name).first()

    @classmethod
    def check_for_kind_donation(cls, _id: int) -> str:
        return cls.query.filter_by(id=_id).mode_name

    @classmethod
    def find_mode_name_by_id(cls, _id: int) -> str:
        return cls.query.filter_by(id=_id).first().mode_name

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
