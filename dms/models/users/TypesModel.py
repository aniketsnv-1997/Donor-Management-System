from dms import db
from .ProjectsModel import ProjectsModel

class TypesModel(db.Model):
    __tablename__ = 'types'

    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.String(50), unique=True, nullable=False)
    create_date = db.Column(db.DateTime, unique=False, nullable=False)
    update_date = db.Column(db.DateTime, unique=False, nullable=True)

    projects = db.relationship('ProjectsModel', backref='types')

    def __init__(self, _id, type_name, description, create_date, update_date):
        self.id = _id
        self.type_name = type_name
        self.description = description
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_types(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(type_name=name).first()

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()
