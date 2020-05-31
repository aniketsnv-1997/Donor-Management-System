from dms import db


class StateModel(db.Model):
    __tablename__ = "states"

    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(20), unique=True, nullable=False)
    country_id = db.Column(
        db.Integer, db.ForeignKey("country.id"), unique=False, nullable=False
    )
    create_date = db.Column(db.DateTime, unique=False, nullable=False)
    update_date = db.Column(db.DateTime, unique=False, nullable=True)

    donors = db.relationship("DonorsModel", backref="state", lazy="dynamic")

    def __init__(self, _id: int, state_name: str, create_date, update_date):
        self.id = _id
        self.state_name = state_name
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_states(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, state_name: str):
        return cls.query.filter_by(state_name=state_name).first()

    def save_to_database(self) -> None:
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self) -> None:
        db.session.delete(self)
        db.session.commit()
