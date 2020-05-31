from datetime import timedelta

from flask import Flask
from flask_mail import Mail
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
# from flask_marshmallow import Marshmallow

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/dms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config[
    "PROPAGATE_EXCEPTIONS"
] = True  # This line enables the Flask app to identify errors and exceptions
# related to FlaskJWT and then report them accordingly
app.secret_key = "aniket"
app.config["JWT_SECRET_KEY"] = "aniket"
app.config["JWT_AUTH_URL_RULE"] = "/login"
app.config["JWT_EXPIRATION_DELTA"] = timedelta(seconds=1800)
app.config["JWT_BLACKLIST_ENABLE"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'aniketsvsmecc@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'aniketsvsmecc@gmail.com' # enter your email here
app.config['MAIL_PASSWORD'] = 'vian020213' # enter your password here
db = SQLAlchemy(app)
api = Api(app)
mail = Mail(app)
# ma = Marshmallow()

from dms.models.donations.DonationsModel import DonationsModel
from dms.models.donations.KindDonationsModel import KindDonationModel
from dms.models.donations.ModesModel import MM
from dms.models.donors.CountryModel import CountryModel
from dms.models.donors.DonorsModel import DonorsModel
from dms.models.donors.ReferencesModel import ReferenceModel
from dms.models.donors.StatesModel import StateModel
from dms.models.users.ProjectsModel import ProjectsModel
from dms.models.users.RightsModel import RightsModel
from dms.models.users.RolesModel import RolesModel
from dms.models.users.TypesModel import TypesModel
from dms.models.users.UsersModel import UsersModel


def create_db():
    db.create_all()
    print("DB Created Successfully")


@app.before_first_request
def db_creation_command():
    create_db()


jwt = JWTManager(app)
