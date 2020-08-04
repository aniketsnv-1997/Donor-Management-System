from datetime import datetime as dt

from flask import make_response, render_template
from flask_restful import request, Resource

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


class ShowRolesForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("./users/forms/add_role.html", title="Add Role"), 200, headers)


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
        role_name = ""
        description = ""

        if request.method == "POST":
            role_name = request.form.get("role_name")
            description = request.form.get("description")

        role = RolesModel.find_by_name(role_name)

        if role:
            message = f"The role {role.role_name} is already present in the system"
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('./users/view after add/new_role_added.html',
                                                 message=message,), 405, headers)

        else:
            new_role = RolesModel(
                None, role_name, description, dt.now(), None
            )

            new_role.save_to_database()
            new_role_added = RolesModel.find_by_name(role_name)
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('./users/view after add/new_role_added.html',
                                                 role_name=new_role_added.role_name,
                                                 description=new_role_added.description), 201, headers)
            # return pdfkit.from_url("http://127.0.0.1:5000/add%role", "test.pdf")

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
