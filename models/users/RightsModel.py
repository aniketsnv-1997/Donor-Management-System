from database import db


class RightsModel(db.Model):
    __tablename__ = 'rights'

    id = db.Column(db.INTEGER, primary_key=True)
    rights_name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.TEXT(50), unique=True, nullable=False)
    create_date = db.Column(db.DATE, unique=False, nullable=False)
    update_date = db.Column(db.DATE, unique=False, nullable=True)

    users = db.relationship('UsersModel', lazy='dynamic')

    def __init__(self, _id, rights_name, description, create_date, update_date):
        self.id = _id
        self.rights_name = rights_name
        self.description = description
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_rights(cls):
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(rights_name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()
