from database import db


class DonorsModel(db.Model):
    __tablename__ = 'donors'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.VARCHAR(20), nullable=False, unique=False)
    email_address = db.Column(db.VARCHAR(50), unique=True, nullable=False)
    date_of_birth = db.Column(db.DATE, unique=False, nullable=False)
    date_of_anniversary = db.Column(db.DATE, unique=False, nullable=False)
    pan = db.Column(db.CHAR(10), unique=True, nullable=False)
    uid = db.Column(db.BIGINT, unique=True, nullable=False)
    country_code = db.Column(db.INT, unique=False, nullable=False)
    phone_number = db.Column(db.VARCHAR(12), unique=True, nullable=False)
    reference_id = db.Column(db.INT, db.ForeignKey('references.id'), unique=True, nullable=False)
    other_reference = db.Column(db.VARCHAR(20), unique=False, nullable=True)
    referrer_name = db.Column(db.VARCHAR(20), nullable=True, unique=False)
    address_line_1 = db.Column(db.VARCHAR(50), nullable=False, unique=False)
    address_line_2 = db.Column(db.VARCHAR(50), nullable=True, unique=False)
    city = db.Column(db.VARCHAR(30), unique=False, nullable=False)
    state_id = db.Column(db.INT, db.ForeignKey('states.id'), unique=False, nullable=False)
    country_id = db.Column(db.INT, db.ForeignKey('country.id'), unique=False, nullable=False)
    pincode = db.Column(db.BIGINT, unique=False, nullable=False)
    create_date = db.Column(db.DATE, unique=False, nullable=False)
    update_date = db.Column(db.DATE, unique=False, nullable=False)

    reference = db.relationship('ReferenceModel')
    state = db.relationship('StateModel')
    country = db.relationship('CountryModel')

    def __init__(self, _id, name, email_address, date_of_birth, date_of_anniversary, pan, uid, country_code,
                 phone_number, reference, other_reference, referrer_name, address_line_1, address_line_2, city,
                 state, country, pincode, create_date, update_date):
        self.id = _id
        self.name = name
        self.email_address = email_address
        self.date_of_birth = date_of_birth
        self.date_of_anniversary = date_of_anniversary
        self.pan = pan
        self.uid = uid
        self.country_code = country_code
        self.phone_number = phone_number
        self.reference = reference
        self.other_reference = other_reference
        self.referrer_name = referrer_name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.country = country
        self.pincode = pincode
        self.create_Date = create_date
        self.update_date = update_date

    @classmethod
    def find_by_email_address(cls, email_address):
        return cls.query.filter_by(email_address=email_address).first()

    @classmethod
    def get_all_donors(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()
