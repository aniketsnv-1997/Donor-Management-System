from dms.app import db


class OnlineDonationsModel(db.Model):
    __tablename__ = "online_donations"

    id = db.Column(db.Integer, primary_key=True)
    date_of_credit = db.Column(db.DATETIME, unique=False, nullable=False)
    transaction_id = db.Column(db.String(10), unique=True, nullable=False)
    donation_id = db.Column(
        db.Integer, db.ForeignKey("donations.id"), unique=False, nullable=True
    )
    create_date = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(
        self,
        _id: int,
        date_of_credit: str,
        transaction_id: str,
        donation_id: int,
        create_date: str,
    ):
        self.id = _id
        self.date_of_credit = date_of_credit
        self.transaction_id = transaction_id
        self.donation_id = donation_id
        self.create_date = create_date

    @classmethod
    def get_all_online_donations(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_donation_id(cls, donation_id: int):
        return cls.query.filter_by(donation_id=donation_id).all()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
