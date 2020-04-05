from database import db


class DonationsModel(db.Model):
    __tablename__ = 'donation'

    id = db.Column(db.INTEGER, primary_key=True)
    date_of_donation = db.Column(db.DATE, unique=False, nullable=False)
    mode_id = db.Column(db.INT, db.ForeignKey('modes_of_donation.id'), nullable=False, unique=False)
    amount_in_figures = db.Column(db.BIGINT, nullable=False, unique=False)
    amount_in_words = db.Column(db.VARCHAR(30), nullable=False, unique=False)
    cheque_number = db.Column(db.VARCHAR(8), nullable=True, unique=True)
    cheque_date = db.Column(db.DATE, nullable=True, unique=False)
    donor_bank = db.Column(db.VARCHAR(20), nullable=True, unique=False)
    project_id = db.Column(db.INT, db.ForeignKey('projects.id'), nullable=False, unique=False)
    donor_id = db.Column(db.INT, db.ForeignKey('donors.id'), nullable=False, unique=False)

    project = db.relationship("ProjectsModel")
    mode = db.relationship("MM")
    donor = db.relationship("DonorsModel")

    kind_donations = db.relationship('KindDonationModel', lazy='dynamic')

    def __init__(self, _id, date_of_donation, mode_id, amount_in_figures, amount_in_words, cheque_number, cheque_date,
                 donor_bank, project_id, donor_id):
        self.id = _id,
        self.date_of_donation = date_of_donation,
        self.mode_id = mode_id,
        self.amount_in_figures = amount_in_figures,
        self.amount_in_words = amount_in_words,
        self.cheque_number = cheque_number,
        self.cheque_date = cheque_date,
        self.donor_bank = donor_bank,
        self.project_id = project_id,
        self.donor_id = donor_id

    @classmethod
    def get_all_donations(cls):
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
