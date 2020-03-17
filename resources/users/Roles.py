from flask_restful import reqparse, Resource
from datetime import datetime as dt

from models.users.RolesModel import RolesModel


class Roles(Resource):

    def get(self):
        roles = RolesModel.get_all_roles()
        roles_list = []

        # TODO Use LIST Comprehension for returning the roles

        for role in roles:
            roles_list.append({"id": role.id, "name": role.role_name, "description": role.description,
                               "create_date": str(role.create_date), "update_date": str(role.update_date)})

        return {"roles": roles_list}, 200


class SingleRole(Resource):

    def get(self, name):
        role = RolesModel.find_by_name(name)

        return {"id": role.id, "name": role.role_name, "description": role.description,
                "create_date": str(role.create_date), "update_date": str(role.update_date)}, 200

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str, required=True, help='This is a mandatory field to be filled')

        data = parser.parse_args()

        if RolesModel.find_by_name(name):
            return {"message": f"Role with name {name} is already present in the system!"}, 401

        new_role = RolesModel(None, name, data['description'], dt.date(dt.now()), None)
        new_role.save_to_database()
        return SingleRole.get(self, name), 201

    def delete(self, name):
        role = RolesModel.find_by_name(name)
        if role is None:
            return {"message": f"Role with name {name} is not present in the system!"}, 401

        role.remove_from_database()

        return 204

    def put(self, name):
        pass
