from dms import db


class KindDonationModel(db.Model):
    __tablename__ = "kind_donations"

    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(20), unique=False, nullable=False)
    quantity = db.Column(db.Float, unique=False, nullable=False)
    unit = db.Column(db.String(5), unique=False, nullable=False)
    donation_id = db.Column(
        db.Integer, db.ForeignKey("donations.id"), unique=False, nullable=True
    )
    create_date = db.Column(db.DateTime, unique=False, nullable=False)

    def __init__(
        self,
        _id: int,
        item: str,
        quantity: float,
        unit: str,
        donation_id: int,
        create_date,
    ):
        self.id = _id
        self.item = (item,)
        self.quantity = (quantity,)
        self.unit = unit
        self.donation_id = donation_id
        self.create_date = create_date

    @classmethod
    def get_all_kind_donations(cls):
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
