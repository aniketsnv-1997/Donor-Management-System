from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.users.ProjectsModel import ProjectsModel


class Projects(Resource):

    def get(self):
        projects = ProjectsModel.get_all_projects()
        project_list = []

        # TODO Use LIST Comprehension for returning the projects

        for project in projects:
            project_list.append({"id": project.id, "name": project.projects_name, "description": project.description,
                                 "create_date": str(project.create_date), "update_date": str(project.update_date)})

        #project_list = []
        return {"projects": project_list}, 200


class SingleProject(Resource):

    def get(self, name):
        project = ProjectsModel.find_by_name(name)

        return {"id": project.id, "name": project.role_name, "description": project.description,
                "type_id": project.type_id, "create_date": str(project.create_date), "update_date": str(project.update_date)}, 200

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('type_id', type=int, required=True, help='This is a mandatory field to be filled')
        data = parser.parse_args()

        if ProjectsModel.find_by_name(name):
            return {"message": f"Project with name {name} is already present in the system!"}, 401

        new_project = ProjectsModel(None, name, data['description'], data['type_id'], dt.date(dt.now()), None)
        new_project.save_to_database()
        return SingleProject.get(self, name), 201

    def delete(self, name):
        project = ProjectsModel.find_by_name(name)
        if project is None:
            return {"message": f"project with name {name} is not present in the system!"}, 401

        project.remove_from_database()

        return 204

    def put(self, name):
        pass
