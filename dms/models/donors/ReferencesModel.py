from dms import db
from .DonorsModel import DonorsModel


class ReferenceModel(db.Model):
    __tablename__ = "references"

    id = db.Column(db.Integer, primary_key=True)
    reference_name = db.Column(db.String(10), unique=True, nullable=False)
    create_date = db.Column(db.DateTime, unique=False, nullable=False)
    update_date = db.Column(db.DateTime, unique=False, nullable=True)

    donors = db.relationship("DonorsModel", backref="reference")

    def __init__(self, _id: int, reference_name: str, create_date, update_date):
        self.id = _id
        self.reference_name = reference_name
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_references(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, reference_name: str):
        return cls.query.filter_by(reference_name=reference_name).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
