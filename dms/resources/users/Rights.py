from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.users.RightsModel import RightsModel


class Rights(Resource):
    def get(self):
        rights = RightsModel.get_all_rights()
        right_list = []

        # TODO Use LIST Comprehension for returning the RIGHTS

        if rights:
            for right in rights:
                right_list.append(
                    {
                        "id": right.id,
                        "name": right.rights_name,
                        "description": right.description,
                        "create_date": str(right.create_date),
                        "update_date": str(right.update_date),
                    }
                )

            return {"rights": right_list}, 200

        return {"message": f"No Rights present in the system!"}, 404


class SingleRight(Resource):
    def get(self, _id):
        right = RightsModel.find_by_id(_id)

        if right:
            return (
                {
                    "id": right.id,
                    "name": right.role_name,
                    "description": right.description,
                    "create_date": str(right.create_date),
                    "update_date": str(right.update_date),
                },
                200,
            )

        return {"message": f"No Right with {_id} is present in the system!"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "right_name",
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

        right = RightsModel.find_by_name(data["right_name"])

        if right:
            return (
                {
                    "message": f"Right {data['right_name']} is already present in the system!"
                },
                400,
            )

        new_right = RightsModel(
            None, data["right_name"], data["description"], dt.now(), None
        )

        new_right.save_to_database()
        new_right_added = RightsModel.find_by_name(data["right_name"])

        return (
            {
                "id": new_right_added.id,
                "right_name": new_right_added.rights_name,
                "description": new_right_added.description,
                "create_date": str(new_right_added.create_date),
                "update_date": str(new_right_added.update_date),
            },
            201,
        )

    def delete(self, _id):
        right = RightsModel.find_by_name(_id)

        if right:
            deleted_right = right.rights_name
            right.remove_from_database()

            return (
                {"message": f"Right {deleted_right} is not present in the system!"},
                204,
            )

        return {"message": f"Right with id {_id} is not present in the system!"}, 400
