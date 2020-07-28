from flask_restful import reqparse, Resource
from flask import render_template, make_response, request
from datetime import datetime as dt

from dms.models.users.ProjectsModel import ProjectsModel
from dms.models.users.TypesModel import TypesModel


class Projects(Resource):
    def get(self):
        projects = ProjectsModel.get_all_projects()
        project_list = []

        # TODO Use LIST Comprehension for returning the projects

        if projects:
            for project in projects:
                project_list.append(
                    {
                        "id": project.id,
                        "name": project.project_name,
                        "description": project.description,
                        "create_date": str(project.create_date),
                        "update_date": str(project.update_date),
                    }
                )

            return {"projects": project_list}, 200

        return {"message": f"No projects exist in the system as of now!"}, 404


class ShowProjectsForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("./users/forms/project_form.html", title="Add Project/Activity/Type",
                                             types=TypesModel.get_all_types()), 200, headers)


class SingleProject(Resource):
    def get(self, _id):
        project = ProjectsModel.find_by_id(_id)

        if project:
            return (
                {
                    "id": project.id,
                    "name": project.project_name,
                    "description": project.description,
                    "type_id": project.type_id,
                    "create_date": str(project.create_date),
                    "update_date": str(project.update_date),
                },
                200,
            )

        return {"message": f"Project with {_id} is not present in the system!"}, 404

    def post(self):
        project_name = ""
        description = ""
        type_id = 0

        if request.method == "POST":
            project_name = request.form.get("project_name")
            description = request.form.get("description")
            type_id = request.form.get("type_id")

        if ProjectsModel.find_by_name(project_name):
            message = f"The project {project_name} is already present in the system"
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('./users/view after add/new_project_added.html',
                                                 message=message, ), 201, headers)

        new_project = ProjectsModel(
            None, project_name, description, type_id, dt.now(), None
        )
        new_project.save_to_database()

        new_project_added = ProjectsModel.find_by_name(project_name)

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('./users/view after add/new_project_added.html',
                                             project_name=new_project_added.project_name,
                                             description=new_project_added.description,
                                             type_name=TypesModel.find_by_id(new_project.type_id).type_name, ),
                             201, headers)

    def delete(self, _id):
        project = ProjectsModel.find_by_id(_id)

        if project:
            deleted_project = project.project_name
            project.remove_from_database()
            return (
                {
                    "message": f"project {deleted_project} has been successfully deleted from the system!"
                },
                200,
            )

        return {"message": f"Project with id {_id} is not present in the system!"}, 400
