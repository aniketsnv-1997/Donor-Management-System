from flask_restful import reqparse, Resource
from datetime import datetime as dt

from models.donations.ModesModel import ModesModel


class Modes(Resource):

    def get(self):
        modes = ModesModel.get_all_modes()
        modes_list = []

        # TODO Use LIST Comprehension for returning the modes

        for mode in modes:
            modes_list.append({"id": mode.id, "name": mode.mode_name, "create_date": str(mode.create_date),
                               "update_date": str(mode.update_date)})

        return {"modes": modes_list}, 200


class SingleMode(Resource):

    def get(self, name):
        mode = ModesModel.find_by_name(name)

        return {"id": mode.id, "name": mode.mode_name, "create_date": str(mode.create_date),
                "update_date": str(mode.update_date)}, 200

    def post(self, name):

        if ModesModel.find_by_name(name):
            return {"message": f"Mode with name {name} is already present in the system!"}, 401

        new_mode = ModesModel(None, name, dt.date(dt.now()), None)
        new_mode.save_to_database()
        return SingleMode.get(self, name), 201

    def delete(self, name):
        mode = ModesModel.find_by_name(name)
        if mode is None:
            return {"message": f"Mode with name {name} is not present in the system!"}, 401

        mode.remove_from_database()

        return 204

    def put(self, name):
        pass
