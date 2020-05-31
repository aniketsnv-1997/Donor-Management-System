from flask import jsonify
from flask_restful import reqparse, Resource
from datetime import datetime as dt

from ...models.donations.ModesModel import MM


class Modes(Resource):
    def get(self):
        modes = MM.get_all_modes()
        modes_list = []

        # TODO Use LIST Comprehension for returning the modes

        if modes:
            for mode in modes:
                modes_list.append(
                    {
                        "id": mode.id,
                        "name": mode.mode_name,
                        "create_date": str(mode.create_date),
                        "update_date": str(mode.update_date),
                    }
                )

            return {"modes": modes_list}, 200

        return (
            {
                "message": "No modes of donation exists in the system! Please add a new mode of donation"
            },
            404,
        )


class SingleMode(Resource):
    def get(self, _id):
        mode = MM.find_by_id(_id)

        if mode:
            return (
                {
                    "id": mode.id,
                    "name": mode.mode_name,
                    "create_date": str(mode.create_date),
                    "update_date": str(mode.update_date),
                },
                200,
            )

        return (
            {"message": f"No mode of donation with id {_id} present in the system"},
            404,
        )

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "mode_name", type=str, required=True, help="This is a mandatory field!"
        )

        data = parser.parse_args()

        if MM.find_by_name(data["mode_name"]):
            return (
                {
                    "message": f"Mode with name {data['mode_name']} is already present in the system!"
                },
                400,
            )

        new_mode = MM(None, data["mode_name"], dt.now(), None)
        new_mode.save_to_database()

        new_mode_added = MM.find_by_name(data["mode_name"])
        return (
            {
                "id": new_mode_added.id,
                "mode_name": new_mode_added.mode_name,
                "create_date": str(new_mode_added.create_date),
                "update_date": new_mode_added.update_date,
            },
            201,
        )

    def delete(self, _id):
        mode = MM.find_by_id(_id)
        if mode:
            deleted_mode_name = mode.mode_name
            mode.remove_from_database()
            return (
                {
                    "message": f"{deleted_mode_name} mode of donation has been deleted successfully from the system!"
                },
                200,
            )

        return {"message": "Mode not present in the system!"}, 400
