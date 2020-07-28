from flask import jsonify, make_response, render_template
from flask_restful import Resource, request
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


class ShowDonationModesForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("./donations/forms/add_donation_mode.html", title="Add a donation mode"), 200, headers)


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
        mode_name = ""

        if request.method == "POST":
            mode_name = request.form.get("mode_name")

        if MM.find_by_name(mode_name):
            return (
                {
                    "message": f"Mode with name {mode_name} is already present in the system!"
                },
                400,
            )

        new_mode = MM(None, mode_name, dt.now(), None)
        new_mode.save_to_database()

        new_mode_added = MM.find_by_name(mode_name)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('./users/view after add/new_mode_added.html',
                                             title="New Mode Added Details",
                                             mode_name=new_mode_added.mode_name), 200, headers)

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
