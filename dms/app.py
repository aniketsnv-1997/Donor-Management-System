from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/dms"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True  # This line enables the Flask app to identify errors and exceptions
# related to FlaskJWT and then report them accordingly


# Authentication related configuration values
app.secret_key = "aniket"
app.config["JWT_SECRET_KEY"] = "aniket"
app.config["JWT_AUTH_URL_RULE"] = "/login"
ACCESS_EXPIRES = timedelta(minutes=15)
REFRESH_EXPIRES = timedelta(days=30)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = ACCESS_EXPIRES
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = REFRESH_EXPIRES
app.config["JWT_BLACKLIST_ENABLE"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]

# Linkages of the functionalities with the main flask app
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)


def create_db():
    db.create_all()
    print("DB Created Successfully")


@app.before_first_request
def db_creation_command():
    create_db()


jwt = JWTManager(app)


# Third Party Library Imports
from flask import jsonify

# Imports from user related Resources
from dms.resources.users.Projects import Projects, SingleProject, ShowProjectsForm
from dms.resources.users.Rights import Rights, SingleRight, ShowAccessRightsForm
from dms.resources.users.Types import Types, SingleType, ShowTypesForm
from dms.resources.users.Roles import Roles, SingleRole, ShowRolesForm
from dms.resources.users.User import (
    Users,
    ShowUsersForm,
    SingleUser,
    UserLogin,
    UserCredentials,
    TokenRefresh,
    UserLogout,
    ShowChangePasswordForm
)

# Imports from donor related Resources
from dms.resources.donors.Donors import Donors, SingleDonor, ShowDonorsForm
from dms.resources.donors.References import Reference, SingleReference, ShowReferenceForm
from dms.resources.donors.States import State, SingleState
from dms.resources.donors.Country import Country, SingleCountry

# Imports from donations related Resources
from dms.resources.donations.Donations import Donation, SingleDonation, ShowDonationsForm
from dms.resources.donations.KindDonations import KindDonations, SingleKindDonation
from dms.resources.donations.Modes import Modes, SingleMode, ShowDonationModesForm

from dms.logout import BLACKLIST
from dms.resources.homepage import HomePage


# Used to add some more values and functionalities to the existing JWT token, like admin and user access
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # TODO: Instead of 1, write the query to get id where user name is Vaishali Modak
    if identity == 1:
        return {"is_admin": True}

    return {"is_admin": False}


# To be used to check whether a token is logged out or not
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


# When JWT token sent by user to server is expired (a JWT token expired after 5 minutes)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": "The token has expired", "error": "token_expired"}), 401

# When the user does not send any token to the server
@jwt.unauthorized_loader
def no_token_callback():
    return jsonify({"message": "No token provided", "error": "no_token_received"})

# When the server needs a fresh token
@jwt.needs_fresh_token_loader
def no_fresh_token_callback():
    return jsonify({"message": "Send a fresh token", "error": "fresh_token_required"})

# When the server gets a revoked token from user, used in case of logout
@jwt.revoked_token_loader
def revoked_token_callback():
    return (
        jsonify(
            {
                "message": "You have been logged out from the system",
                "error": "revoked_token",
            }
        ),
        401,
    )


api.add_resource(HomePage, "/")

api.add_resource(Users, "/users")
api.add_resource(ShowUsersForm, "/add%a%new%user")
api.add_resource(SingleUser, "/users/<int:_id>", "/users")
api.add_resource(UserCredentials, "/change%password")
api.add_resource(ShowChangePasswordForm, "/show-change-password-form")

api.add_resource(Projects, "/projects")
api.add_resource(ShowProjectsForm, "/add%project")
api.add_resource(SingleProject, "/projects/<int:_id>", "/projects")

api.add_resource(Roles, "/roles")
api.add_resource(ShowRolesForm, "/add%role")
api.add_resource(SingleRole, "/roles/<int:_id>", "/roles")

api.add_resource(Rights, "/rights")
api.add_resource(ShowAccessRightsForm, "/add%access%rights")
api.add_resource(SingleRight, "/rights/<int:_id>", "/rights")

api.add_resource(Types, "/types")
api.add_resource(ShowTypesForm, "/add%project%type")
api.add_resource(SingleType, "/types/<int:_id>", "/types")

api.add_resource(Country, "/country")
api.add_resource(SingleCountry, "/country/<int:_id>", "/country")

api.add_resource(Reference, "/references")
api.add_resource(ShowReferenceForm, "/add%a%new%reference")
api.add_resource(SingleReference, "/references/<int:_id>", "/references")

api.add_resource(State, "/states")
api.add_resource(SingleState, "/states/<int:_id>", "/states")

api.add_resource(Donors, "/donors")
api.add_resource(ShowDonorsForm, "/add-a-new-donor")
api.add_resource(SingleDonor, "/donors/<int:_id>", "/donors")

api.add_resource(Donation, "/donations")
api.add_resource(ShowDonationsForm, "/add-a-new-donation")
api.add_resource(SingleDonation, "/donations/<int:_id>", "/donations")

api.add_resource(KindDonations, "/kind_donations")
api.add_resource(SingleKindDonation, "/kind_donations/<int:id>")

api.add_resource(Modes, "/modes")
api.add_resource(ShowDonationModesForm, "/add%a%donation%mode")
api.add_resource(SingleMode, "/modes/<int:_id>", "/modes")

api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    db.init_app(app)
    app.run()
