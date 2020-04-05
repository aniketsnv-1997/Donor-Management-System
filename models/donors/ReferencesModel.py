from database import db


class ReferenceModel(db.Model):
    __tablename__ = 'references'

    id = db.Column(db.INTEGER, primary_key=True)
    reference_name = db.Column(db.VARCHAR(10), unique=True, nullable=False)
    create_date = db.Column(db.DATE, unique=False, nullable=False)
    update_date = db.Column(db.DATE, unique=False, nullable=True)

    donors = db.relationship('DonorsModel', lazy='dynamic')

    def __init__(self, _id, reference_name, create_date, update_date):
        self.id = _id
        self.reference_name = reference_name
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_references(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, reference_name):
        return cls.query.filter_by(reference_name=reference_name).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()
