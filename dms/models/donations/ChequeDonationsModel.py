
from dms.app import db


class ChequeDonationsModel(db.Model):
    __tablename__ = "cheque_donation"

    id = db.Column(db.Integer, primary_key=True)
    cheque_number = db.Column(db.BigInteger, unique=True, nullable=True)
    cheque_date = db.Column(db.DateTime, unique=False, nullable=False)
    amount_in_figures = db.Column(db.BigInteger, nullable=False, unique=False)
    amount_in_words = db.Column(db.String(30), nullable=False, unique=False)
    date_of_credit = db.Column(db.DateTime, unique=False, nullable=False)
    donor_bank = db.Column(db.String(50), unique=False, nullable=False)
    donation_id = db.Column(
        db.Integer, db.ForeignKey("donations.id"), unique=False, nullable=True
    )
    create_date = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(self, _id, cheque_number, cheque_date, amount_in_figures, amount_in_words, date_of_credit, donor_bank,
                 donation_id, create_date):
        self.id = _id
        self.cheque_number = cheque_number
        self.cheque_date = cheque_date
        self.amount_in_figures = amount_in_figures
        self.amount_in_words = amount_in_words
        self.date_of_credit = date_of_credit
        self.donor_bank = donor_bank
        self.donation_id = donation_id
        self.create_date = create_date

    @classmethod
    def get_all_cheque_donations(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def get_by_donation_id(cls, donation_id: int):
        return cls.query.filter_by(donation_id=donation_id).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()