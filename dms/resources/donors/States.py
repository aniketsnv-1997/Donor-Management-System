from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.donors.StatesModel import StateModel


class State(Resource):
    def get(self):
        states = StateModel.get_all_states()
        states_list = []

        # TODO Use LIST Comprehension for returning the states

        for state in states:
            states_list.append(
                {
                    "id": state.id,
                    "name": state.state_name,
                    "country_id": state.country_id,
                    "create_date": str(state.create_date),
                    "update_date": str(state.update_date),
                }
            )

        return {"states": states_list}, 200


class SingleState(Resource):
    def get(self, name):
        state = StateModel.find_by_name(name)

        return (
            {
                "id": state.id,
                "name": state.state_name,
                "country_id": state.country_id,
                "create_date": str(state.create_date),
                "update_date": str(state.update_date),
            },
            200,
        )

    def post(self, name):
        parser = reqparse.RequestParser()

        parser.add_argument(
            "country_id",
            type=int,
            required=True,
            help="This is a mandatory field to be filled",
        )
        data = parser.parse_args()

        if StateModel.find_by_name(name):
            return (
                {
                    "message": f"State with name {name} is already present in the system!"
                },
                401,
            )

        new_state = StateModel(None, name, data["country_id"], dt.date(dt.now()), None)
        new_state.save_to_database()
        return SingleState.get(self, name), 201

    def delete(self, name):
        state = StateModel.find_by_name(name)
        if state is None:
            return (
                {"message": f"State with name {name} is not present in the system!"},
                401,
            )

        state.remove_from_database()

        return 204

    def put(self, name):
        pass
