from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.users.RolesModel import RolesModel


class Roles(Resource):
    def get(self):
        roles = RolesModel.get_all_roles()
        roles_list = []

        # TODO Use LIST Comprehension for returning the roles

        if roles:
            for role in roles:
                roles_list.append(
                    {
                        "id": role.id,
                        "name": role.role_name,
                        "description": role.description,
                        "create_date": str(role.create_date),
                        "update_date": str(role.update_date),
                    }
                )

            return {"roles": roles_list}, 200

        return {"message": f"No roles present in the system!"}, 404


class SingleRole(Resource):
    def get(self, _id):
        role = RolesModel.find_by_id(_id)

        if role:
            return (
                {
                    "id": role.id,
                    "name": role.role_name,
                    "description": role.description,
                    "create_date": str(role.create_date),
                    "update_date": str(role.update_date),
                },
                200,
            )

        return {"message": f"Role with id {_id} is not available in the system!"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "role_name",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "description",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )

        data = parser.parse_args()

        role = RolesModel.find_by_name(data["role_name"])

        if role:
            return (
                {
                    "message": f"Role with name {data['role_name']} is already present in the system!"
                },
                400,
            )

        new_role = RolesModel(
            None, data["role_name"], data["description"], dt.now(), None
        )
        new_role.save_to_database()

        new_role_added = RolesModel.find_by_name(data["role_name"])
        return (
            {
                "id": new_role_added.id,
                "role_name": new_role_added.role_name,
                "description": new_role_added.description,
                "create_date": str(new_role_added.create_date),
                "update_date": str(new_role_added.update_date),
            },
            201,
        )

    def delete(self, _id):
        role = RolesModel.find_by_id(_id)

        if role:
            deleted_role = role.role_name
            role.remove_from_database()

            return (
                {
                    "message": f"Role {deleted_role} has been successfully deleted from the system!"
                },
                204,
            )

        return {"message": f"Role with {_id} is not present in the system!"}, 401
