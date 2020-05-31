from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.users.ProjectsModel import ProjectsModel


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
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
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
        parser.add_argument(
            "type_id",
            type=int,
            required=True,
            help="This is a mandatory field to be filled",
        )
        data = parser.parse_args()

        if ProjectsModel.find_by_name(data["name"]):
            return (
                {
                    "message": f"Project with name {data['name']} is already present in the system!"
                },
                400,
            )

        new_project = ProjectsModel(
            None, data["name"], data["description"], data["type_id"], dt.now(), None
        )
        new_project.save_to_database()

        new_project_added = ProjectsModel.find_by_name(data["name"])
        return (
            {
                "id": new_project_added.id,
                "project_name": new_project_added.project_name,
                "description": new_project_added.description,
                "type_id": new_project_added.type_id,
                "create_date": str(new_project_added.create_date),
                "update_date": str(new_project_added.update_date),
            },
            201,
        )

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
