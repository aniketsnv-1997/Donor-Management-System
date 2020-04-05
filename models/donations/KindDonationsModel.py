from database import db


class KindDonationModel(db.Model):
    __tablename__ = 'kind_donations'

    id = db.Column(db.INTEGER, primary_key=True)
    item = db.Column(db.VARCHAR(20), unique=False, nullable=False)
    quantity = db.Column(db.FLOAT, unique=False, nullable=False)
    unit = db.Column(db.VARCHAR(5), unique=False, nullable=False)
    donation_id = db.Column(db.INT, db.ForeignKey('donations.id'), unique=False, nullable=True)
    create_date = db.Column(db.DATE, unique=False, nullable=False)

    donations = db.relationship('DonationsModel')

    def __init__(self, _id, item, quantity, unit, donation_id, create_date):
        self.id = _id
        self.item = item,
        self.quantity = quantity,
        self.unit = unit
        self.donation_id = donation_id
        self.create_date = create_date

    @classmethod
    def get_all_kind_donations(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()
