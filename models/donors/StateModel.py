from database import db


class StateModel(db.Model):
    __tablename__ = 'states'

    id = db.Column(db.INTEGER, primary_key=True)
    state_name = db.Column(db.VARCHAR(20), unique=True, nullable=False)
    country_id = db.Column(db.INT, db.ForeignKey('country.id'), unique=False, nullable=False)
    create_date = db.Column(db.DATE, unique=False, nullable=False)
    update_date = db.Column(db.DATE, unique=False, nullable=True)

    donors = db.relationship('DonorsModel', lazy='dynamic')
    country = db.relationship('CountryModel')

    def __init__(self, _id, state_name, create_date, update_date):
        self.id = _id
        self.state_name = state_name
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_states(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, state_name):
        return cls.query.filter_by(state_name=state_name).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()