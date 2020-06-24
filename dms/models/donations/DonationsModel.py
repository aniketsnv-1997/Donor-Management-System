from dms import db
from .KindDonationsModel import KindDonationModel


class DonationsModel(db.Model):
    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, unique=False)
    date_of_donation = db.Column(db.DateTime, unique=False, nullable=False)
    mode_id = db.Column(
        db.Integer, db.ForeignKey("modes_of_donation.id"), nullable=False, unique=False
    )
    amount_in_figures = db.Column(db.Integer, nullable=False, unique=False)
    amount_in_words = db.Column(db.String(30), nullable=False, unique=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False, unique=False
    )
    donor_id = db.Column(
        db.Integer, db.ForeignKey("donors.id"), nullable=False, unique=False
    )
    create_date = db.Column(db.DateTime, unique=False, nullable=False)

    kind_donations = db.relationship(
        "KindDonationModel", backref="donation", lazy="dynamic"
    )

    cheque_donations = db.relationship(
        "ChequeDonationsModel", backref="donation", lazy="dynamic"
    )

    def __init__(
        self,
        _id: int,
        donation_title: str,
        date_of_donation,
        mode_id: int,
        amount_in_figures: int,
        amount_in_words: str,
        project_id: int,
        donor_id: int,
    ):
        self.id = (_id,)
        self.donation_title = (donation_title,)
        self.date_of_donation = (date_of_donation,)
        self.mode_id = (mode_id,)
        self.amount_in_figures = (amount_in_figures,)
        self.amount_in_words = (amount_in_words,)
        self.project_id = (project_id,)
        self.donor_id = donor_id

    @classmethod
    def get_all_donations(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_title(cls, title: str):
        return cls.query.filter_by(donation_title=title).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
