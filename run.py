from dms import app, api, db, jwt

# Third Party Library Imports
from flask import jsonify
from flask_jwt_extended import JWTManager

# Imports from user related Resources
from dms.resources.users.Projects import Projects, SingleProject
from dms.resources.users.Rights import Rights, SingleRight
from dms.resources.users.Types import Types, SingleType
from dms.resources.users.Roles import Roles, SingleRole
from dms.resources.users.User import (
    Users,
    SingleUser,
    UserLogin,
    UserCredentials,
    TokenRefresh,
    UserLogout,
)

# Imports from donor related Resources
from dms.resources.donors.Donors import Donors, SingleDonor
from dms.resources.donors.References import Reference, SingleReference
from dms.resources.donors.States import State, SingleState
from dms.resources.donors.Country import Country, SingleCountry

# Imports from donations related Resources
from dms.resources.donations.Donations import Donation, SingleDonation
from dms.resources.donations.KindDonations import KindDonations, SingleKindDonation
from dms.resources.donations.Modes import Modes, SingleMode

from dms.models.users.UsersModel import UsersModel
from dms.logout import LOGOUT

jwt = JWTManager(app)

# Used to add some more values and functionalities to the existing JWT token, like admin and user access
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # TODO: Instead of 1, write the query to get id where user name is Vaishali Modak
    if identity == 1:
        return {"is_admin": True}

    return {"is_admin": False}


# To be used to check whether a token is logged out or not
@jwt.token_in_blacklist_loader
def check_token_in_logout(decrypted_token):
    return decrypted_token["jti"] in LOGOUT


# When JWT token sent by user to server is expired (a JWT token expired after 5 minutes)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({"message": "The token has expired", "error": "token_expired"}), 401


# When JWT token sent by user to server is not a valid token
# @jwt.invalid_token_loader
# def invalid_token_callback():
#     return jsonify({
#         "message": "Identity verification failed",
#         "error": "token_invalid"
#     })

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


api.add_resource(Users, "/users")
api.add_resource(SingleUser, "/users/<int:_id>", "/users")
api.add_resource(UserCredentials, "/change%password")

api.add_resource(Projects, "/projects")
api.add_resource(SingleProject, "/projects/<int:_id>", "/projects")

api.add_resource(Roles, "/roles")
api.add_resource(SingleRole, "/roles/<int:_id>", "/roles")

api.add_resource(Rights, "/rights")
api.add_resource(SingleRight, "/rights/<int:_id>", "/rights")

api.add_resource(Types, "/types")
api.add_resource(SingleType, "/types/<int:_id>", "/types")

api.add_resource(Country, "/country")
api.add_resource(SingleCountry, "/country/<int:_id>", "/country")

api.add_resource(Reference, "/references")
api.add_resource(SingleReference, "/references/<int:_id>", "/references")

api.add_resource(State, "/states")
api.add_resource(SingleState, "/states/<int:_id>", "/states")

api.add_resource(Donors, "/donors")
api.add_resource(SingleDonor, "/donors/<int:_id>", "/donors")

api.add_resource(Donation, "/donations")
api.add_resource(SingleDonation, "/donations/<int:_id>", "/donations")

api.add_resource(KindDonations, "/kind_donations")
api.add_resource(SingleKindDonation, "/kind_donations/<int:id>")

api.add_resource(Modes, "/modes")
api.add_resource(SingleMode, "/modes/<int:_id>", "/modes")

api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

if __name__ == "__main__":
    db.init_app(app)
    # ma.init_app(app)
    app.run()
