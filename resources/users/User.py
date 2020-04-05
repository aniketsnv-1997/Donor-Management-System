from flask_restful import reqparse, Resource
from datetime import datetime as dt
from flask_jwt_extended import get_jwt_claims
from flask_jwt_extended import jwt_required

from models.users.UsersModel import UsersModel


class Users(Resource):
    # GET method to get the details of all the users
    def get(self):
        users = UsersModel.get_all_users()
        user_list = []

        # TODO Use LIST Comprehension for returning the Users

        if users:
            for user in users:
                user_list.append({"id": user.id, "name": user.name, "email_address": user.email_address,
                                  "role_id": user.role_id, "project_id": user.project_id, "rights_id": user.rights_id,
                                  "create_date": str(user.create_date), "update_date": str(user.update_date)})

            return {"users": user_list}, 200
        return {"message": "No users present in the system as of now"}, 404


class SingleUser(Resource):

    @jwt_required
    # GET method to get the details of a specific users
    def get(self, name):
        user = UsersModel.find_by_name(name)

        if user:
            return {
                    "id": user.id, "name": user.name, "email_address": user.email_address, "password": user.password,
                    "role_id": user.role_id, "project_id": user.project_id, "rights_id": user.rights_id,
                    "create_date": str(user.create_date), "update_date": str(user.update_date)
                   }, 200

        return {"message": f"User with name {name} does not exist in the system!"}, 404

    # POST method to add a new users into system
    def post(self, name):
        # Let us validate the data coming through the request using request parser
        parser = reqparse.RequestParser()
        # parser.add_argument('name', type=str, required=True, help='This is the mandatory field to be filled')
        parser.add_argument('email_address', type=str, required=True, help='This is the mandatory field to be filled')
        parser.add_argument('password', type=str, required=True, help='This is the mandatory field to be filled')
        parser.add_argument('role_id', type=int, required=True, help='This is the mandatory field to be filled')
        parser.add_argument('project_id', type=int, required=True, help='This is the mandatory field to be filled')
        parser.add_argument('rights_id', type=int, required=True, help='This is the mandatory field')

        data = parser.parse_args()

        if UsersModel.find_by_name(name):
            return {"message": f"User with name {name} already exists in the system!"}, 400

        new_user = UsersModel(None, name, data['email_address'], data['password'], data['role_id'], data['project_id'],
                              data['rights_id'], dt.date(dt.now()), None)
        new_user.save_to_database()

        return SingleUser.get(self, name), 201

    @jwt_required
    def delete(self, name):

        claims = get_jwt_claims()
        if claims['is_admin'] != 1:
            return {"message": "Admin privileges required"}, 401

        if UsersModel.find_by_name(name) is None:
            return {"message": f"User with name {name} does not exist in the system!"}, 400

        user = UsersModel.find_by_name(name)
        user.remove_from_database()

        return {"message": "Item deleted"}, 204

    def put(self, name):
        parser = reqparse.RequestParser()
        # parser.add_argument('name', type=str, required=True, help='This is the mandatory field to be filled')
        parser.add_argument('email_address', type=str, required=False, help='This is the mandatory field to be filled')
        parser.add_argument('password', type=str, required=False, help='This is the mandatory field to be filled')
        parser.add_argument('role_id', type=int, required=False, help='This is the mandatory field to be filled')
        parser.add_argument('project_id', type=int, required=False, help='This is the mandatory field to be filled')
        parser.add_argument('rights_id', type=int, required=False, help='This is the mandatory field')

        data = parser.parse_args()

        if UsersModel.find_by_name(name) is None:
            return {"message": f"User with name {name} does not exist in the system!"}, 400
