from flask_restful import reqparse, Resource
from datetime import datetime as dt
from flask_jwt_extended import (
    get_jwt_claims,
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
    fresh_jwt_required,
)
from werkzeug.security import safe_str_cmp

from dms.email import send_email_of_user_registration
from dms.models.users.UsersModel import UsersModel
from dms.models.users.CredentialsModel import CredentialsModel
from dms.models.users.ProjectsModel import ProjectsModel
from dms.models.users.RolesModel import RolesModel
from dms.logout import LOGOUT


# from dms.schemas.users.userschema import UserSchema
# from dms.schemas.users.credentialschema import CredentialSchema

# Serialization and Deserialization, to be worked upon later
# user_schema = UserSchema(unknown='INCLUDE', partial=['update_date'])
# credential_schema = CredentialSchema(unknown='INCLUDE', partial=['update_date'])


class Users(Resource):
    # GET method to get the details of all the users
    def get(self):
        users = UsersModel.get_all_users()
        user_list = []

        # TODO Use LIST Comprehension for returning the Users

        if users:
            for user in users:
                user_list.append(
                    {
                        "id": user.id,
                        "name": user.name,
                        "email_address": user.email_address,
                        "role_id": user.role_id,
                        "project_id": user.project_id,
                        "rights_id": user.rights_id,
                        "create_date": str(user.create_date),
                        "update_date": str(user.update_date),
                    }
                )

            return {"users": user_list}, 200

        return {"message": "No users present in the system as of now"}, 404


class SingleUser(Resource):

    # Implemented using the marshmallow serialization-deserialization concept
    @jwt_required
    def get(self, _id):

        # Used to check that the user is a admin, as only admins are allowed to view details of individual user
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message": "Admin privileges required"}, 401

        user = UsersModel.find_by_id(_id)

        if user:
            return {
                       "id": user.id,
                       "name": user.name,
                       "email_address": user.email_address,
                       "role_id": user.role_id,
                       "project_id": user.project_id,
                       "rights_id": user.rights_id,
                       "create_date": str(user.create_date),
                       "update_date": str(user.update_date),
                   }, 200

        return {"message": f"User with name {_id} does not exist in the system!"}, 404

    # POST method to add a new users into system. Implemented using the marshmallow serialization-deserialization
    # concept
    # @jwt_required
    def post(self):

        # Used to check that the user is a admin, as only admins are allowed to view details of individual user
        # claims = get_jwt_claims()
        # if not claims["is_admin"]:
        #     return {"message": "Admin privileges required"}, 401

        # Let us validate the user_data coming through the request using request parser

        # whenever we get th json data from the user, it passes through marshmallow and gets serialized with the
        # help of user schema. Thus we directly get the object at the backend
        # Also, load() is used to get the data from the user
        # new_user = user_schema.load(request.get_json())
        # user_credentials = credential_schema.load(
        #     {"email_address": new_user.email_address, "password": new_user.password}
        # )

        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='This is the mandatory field to be filled')
        parser.add_argument(
            "email_address",
            type=str,
            required=False,
            help="This is the mandatory field to be filled",
        )
        parser.add_argument('password', type=str, required=False, help='This is the mandatory field to be filled')

        parser.add_argument(
            "role_id",
            type=int,
            required=False,
            help="This is the mandatory field to be filled",
        )

        parser.add_argument(
            "project_id",
            type=int,
            required=False,
            help="This is the mandatory field to be filled",
        )

        parser.add_argument(
            "rights_id", type=int, required=False, help="This is the mandatory field"
        )

        user_data = parser.parse_args()

        if UsersModel.find_by_email_address(user_data.email_address):
            return (
                {
                    "message": f"User with email_address {user_data.email_address} already exists in the system!"
                },
                401,
            )

        new_user_credentials = CredentialsModel(None, user_data['email_address'], user_data['password'], dt.now(), None)
        new_user_credentials.save_to_database()

        user_credential_added = CredentialsModel.get_credential_by_email_address(user_data['email_address'])

        new_user = UsersModel(None, user_data['name'], user_data['email_address'], user_data['role_id'],
                              user_data['project_id'], user_data['rights_id'], user_credential_added.id, dt.now(), None)
        new_user.save_to_database()

        roles = RolesModel.find_by_id(new_user.role_id)
        projects = ProjectsModel.find_by_id(new_user.project_id)

        email_body = f"""
            Hello {user_data.name}
            
            Welcome aboard on the VSM DMS plaform
            
            Your account login credentials are as follows:
            1. Email Address - {user_data.email_address}
            2. Password - {user_data.password}
            
            We request you to change your password after you sign in for the first time into your account
            
            Your other details are as follows: 
            1. Role - {roles.role_name}
            2. Project - {projects.project_name}
            
            If any of your details is wrong, contact Vrushali Modak Mam for the necessary corrections to be made, 
            immediately 
            
            Thanks & Regards
            VSMandal Admin
        """

        send_email_of_user_registration("aniketsvsmecc@gmail.com", [user_data.email_address], email_body)

        return {
                   "id": new_user.id,
                   "name": new_user.name,
                   "email_address": new_user.email_address,
                   "role_id": new_user.role_id,
                   "project_id": new_user.project_id,
                   "rights_id": new_user.rights_id,
                   "create_date": str(new_user.create_date),
                   "update_date": str(new_user.update_date),
               }, 201

        # dump() is used to deserialize an object and convert it into a dictionary/json
        # return user_schema.dump( new_user), 201

    # Admin will have to re-login into the system before he wants to delete an user
    # @fresh_jwt_required
    def delete(self, _id):

        # Used to check that the user is a admin, as only admins are allowed to view details of individual user
        # claims = get_jwt_claims()
        # if not claims["is_admin"]:
        #     return {"message": "Admin privileges required"}, 401

        user = UsersModel.find_by_id(_id)
        user_credential = CredentialsModel.get_credential_by_email_address(user.email_address)

        if user:
            deleted_user = user.name
            user.remove_from_database()
            user_credential.remove_from_database()

            return (
                {
                    "message": f"User  {deleted_user} has been successfully deleted from the system!"
                },
                204,
            )

        return {"message": f"User with id {_id} is not available in the system!"}, 401

    # Update method to be rewritten
    def put(self, _id):
        parser = reqparse.RequestParser()
        # parser.add_argument('name', type=str, required=True, help='This is the mandatory field to be filled')
        parser.add_argument(
            "email_address",
            type=str,
            required=False,
            help="This is the mandatory field to be filled",
        )

        # parser.add_argument('password', type=str, required=False, help='This is the mandatory field to be filled')
        parser.add_argument(
            "role_id",
            type=int,
            required=False,
            help="This is the mandatory field to be filled",
        )
        parser.add_argument(
            "project_id",
            type=int,
            required=False,
            help="This is the mandatory field to be filled",
        )
        parser.add_argument(
            "rights_id", type=int, required=False, help="This is the mandatory field"
        )

        user_data = parser.parse_args()
        user = UsersModel.find_by_id(_id)

        # user_details_to_be_updated = user_schema.load(request.get_json())

        if user:
            user_credential = CredentialsModel.get_credential_by_email_address(user.email_address)

            user.email_address = user_data.email_address
            user.role_id = user_data.role_id
            user.project_id = user_data.project_id
            user.rights_id = user_data.rights_id
            user.update_date = dt.now()

            user_credential.email_address = user_data.email_address

            user.save_to_database()
            user_credential.save_to_database()

            updated_user = UsersModel.find_by_id(_id)
            return {
                       "id": updated_user.id,
                       "name": updated_user.name,
                       "email_address": updated_user.email_address,
                       "role_id": updated_user.role_id,
                       "project_id": updated_user.project_id,
                       "rights_id": updated_user.rights_id,
                       "create_date": str(updated_user.create_date),
                       "update_date": str(updated_user.update_date),
                   }, 200

        return {"message": f"User with id {_id} does not exist in the system!"}, 401


# This resource will be called when the user will want to change his password
class UserCredentials(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "email_address", type=str, required=True, help="This is a required filed"
        )
        parser.add_argument(
            "password", type=str, required=True, help="This is mandatory field"
        )
        parser.add_argument(
            "new_password", type=str, required=True, help="This is a required filed"
        )
        parser.add_argument(
            "confirm_new_password",
            type=str,
            required=True,
            help="This is mandatory field",
        )

        # user_credentials = credential_schema.load(request.get_json())
        user_data = parser.parse_args()

        user_credentials_from_db = UsersModel.find_by_email_address(user_data['email_address'])
        if user_credentials_from_db and user_credentials_from_db.password == user_data['password']:
            if user_data['new_password'] == user_data['confirm_new_password']:
                user_credentials_from_db.password = user_data['new_password']
                user_credentials_from_db.save_to_database()
                return (
                    {
                        "message": f"The password was successfully updated!"
                    },
                    200
                )

            return (
                {
                    "message": "New password and confirm new password do not match with each other!"
                },
                401
            )

        return {
                   "message": "Please enter valid credentials! Bad Request!"
               }, 401


class UserLogin(Resource):
    @classmethod
    def post(cls):
        parser = reqparse.RequestParser()

        parser.add_argument(
            "email_address", type=str, required=True, help="This is a mandatory field"
        )
        parser.add_argument(
            "password", type=str, required=True, help="This is a mandatory field"
        )

        login_details = parser.parse_args()

        # login_user = credential_schema.load(request.get_json())

        user = UsersModel.find_by_email_address()

        # Cloning the functionality of the authenticate() method
        if user and safe_str_cmp(user.password, login_details.password):
            # This is the clone of the identity function
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        # get_raw_jwt() is a dictionary which has a key 'jti' inside it!
        # The value of this 'jti' is specifically the access token which we have to log out!
        logged_out_token = get_raw_jwt()["jti"]
        LOGOUT.add(logged_out_token)
        return {"message": "Successfully logged out from the system!"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
