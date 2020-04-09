from dms import db
from .UsersModel import UsersModel
from ..donations.DonationsModel import DonationsModel


class ProjectsModel(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text, unique=True, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('types.id'), unique=False, nullable=False)
    create_date = db.Column(db.DateTime, unique=False, nullable=False)
    update_date = db.Column(db.DateTime, unique=False, nullable=True)

    users = db.relationship('UsersModel', backref='projects')
    donation_for_project = db.relationship('DonationsModel', backref='project')

    def __init__(self, _id, project_name, description, type_id, create_date, update_date):
        self.id = _id
        self.project_name = project_name
        self.description = description
        self.type_id = type_id
        self.create_date = create_date
        self.update_date = update_date

    @classmethod
    def get_all_projects(cls):
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
