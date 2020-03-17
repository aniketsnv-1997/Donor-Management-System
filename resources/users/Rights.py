from flask_restful import reqparse, Resource
from datetime import datetime as dt

from models.users.RightsModel import RightsModel


class Rights(Resource):

    def get(self):
        rights = RightsModel.get_all_rights()
        right_list = []

        # TODO Use LIST Comprehension for returning the RIGHTS

        for right in rights:
            right_list.append({"id": right.id, "name": right.rights_name, "description": right.description,
                               "create_date": str(right.create_date), "update_date": str(right.update_date)})

        return {"rights": right_list}, 200


class SingleRight(Resource):

    def get(self, name):
        right = RightsModel.find_by_name(name)

        return {"id": right.id, "name": right.role_name, "description": right.description,
                "create_date": str(right.create_date), "update_date": str(right.update_date)}, 200

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str, required=True, help='This is a mandatory field to be filled')

        data = parser.parse_args()

        if RightsModel.find_by_name(name):
            return {"message": f"Right with name {name} is already present in the system!"}, 401

        new_right = RightsModel(None, name, data['description'], dt.date(dt.now()), None)
        new_right.save_to_database()
        return SingleRight.get(self, name), 201

    def delete(self, name):
        right = RightsModel.find_by_name(name)
        if right is None:
            return {"message": f"right with name {name} is not present in the system!"}, 401

        right.remove_from_database()

        return 204

    def put(self, name):
        pass
