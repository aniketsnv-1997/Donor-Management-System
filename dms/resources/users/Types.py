from flask_restful import reqparse, Resource
from datetime import datetime as dt

from ...models.users.TypesModel import TypesModel


class Types(Resource):

    def get(self):
        types = TypesModel.get_all_types()
        type_list = []

        # TODO Use LIST Comprehension for returning the types

        if types:
            for _type in types:
                type_list.append({"id": _type.id, "name": _type.type_name, "description": _type.description,
                                  "create_date": str(_type.create_date), "update_date": str(_type.update_date)})

            return {"types": type_list}, 200
        return {"message": "No types exist in the system as of now"}, 404


class SingleType(Resource):

    def get(self, name):
        _type = TypesModel.find_by_name(name)

        if _type:
            return {"id": _type.id, "name": _type.type_name, "description": _type.description,
                    "create_date": str(_type.create_date), "update_date": str(_type.update_date)}, 200

        return {"message": f"No Type with name {name} exist in the system as of now"}, 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('description', type=str, required=True, help='This is a mandatory field to be filled')

        data = parser.parse_args()

        if TypesModel.find_by_name(name):
            return {"message": f"Type with name {name} is already present in the system!"}, 401

        new_type = TypesModel(None, name, data['description'], dt.date(dt.now()), None)
        new_type.save_to_database()
        return SingleType.get(self, name), 201

    def delete(self, name):
        _type = TypesModel.find_by_name(name)
        if _type is None:
            return {"message": f"type with name {name} is not present in the system!"}, 401

        _type.remove_from_database()

        return 204

    def put(self, name):
        pass
