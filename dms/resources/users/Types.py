from flask_restful import reqparse, Resource
from flask import make_response, render_template
from datetime import datetime as dt

from ...models.users.TypesModel import TypesModel


class Types(Resource):
    def get(self):
        types = TypesModel.get_all_types()
        type_list = []

        # TODO Use LIST Comprehension for returning the types

        if types:
            for _type in types:
                type_list.append(
                    {
                        "id": _type.id,
                        "name": _type.type_name,
                        "description": _type.description,
                        "create_date": str(_type.create_date),
                        "update_date": str(_type.update_date),
                    }
                )

            return {"types": type_list}, 200

        return {"message": "No types exist in the system as of now!"}, 404


class ShowTypesForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("add_types.html", title="Add Types"), 200, headers)


class SingleType(Resource):
    def get(self, _id):
        _type = TypesModel.find_by_id(_id)

        if _type:
            return (
                {
                    "id": _type.id,
                    "name": _type.type_name,
                    "description": _type.description,
                    "create_date": str(_type.create_date),
                    "update_date": str(_type.update_date),
                },
                200,
            )

        return {"message": f"No Type with id {_id} exist in the system as of now"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "type_name",
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

        _type = TypesModel.find_by_name(data["type_name"])
        if _type:
            return (
                {
                    "message": f"Type with name {_type.type_name} is already present in the system!"
                },
                401,
            )

        new_type = TypesModel(
            None, data["type_name"], data["description"], dt.now(), None
        )

        new_type.save_to_database()

        new_type_added = TypesModel.find_by_name(data["type_name"])

        return (
            {
                "id": new_type_added.id,
                "type_name": new_type_added.type_name,
                "description": new_type_added.description,
                "create_date": str(new_type_added.create_date),
                "update_date": str(new_type_added.update_date),
            },
            201,
        )

    def delete(self, _id):
        _type = TypesModel.find_by_id(_id)
        if _type:
            type_tobe_deleted = _type.type_name
            _type.remove_from_database()

            return (
                {
                    "message": f"type {type_tobe_deleted} has been deleted from the system!"
                },
                204,
            )

        return {"message": f"Type with it {_id} is not present in the system!"}, 401
