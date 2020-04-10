from dms import db
from .StatesModel import StateModel


class CountryModel(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(20), unique=True, nullable=False)
    create_date = db.Column(db.Date, unique=False, nullable=False)
    update_date = db.Column(db.Date, unique=False, nullable=True)

    # donors = db.relationship('DonorsModel', lazy='dynamic')
    states = db.relationship('StateModel', backref='country', lazy='dynamic')

    def __init__(self, _id, country_name, create_date, update_date):
        self.id = _id
        self.country_name = country_name
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_country(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, country_name):
        return cls.query.filter_by(country_name=country_name).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()