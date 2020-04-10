from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.donors.ReferencesModel import ReferenceModel


class Reference(Resource):

    def get(self):
        references = ReferenceModel.get_all_references()
        references_list = []

        # TODO Use LIST Comprehension for returning the references
        if references:
            for reference in references:
                references_list.append({"id": reference.id, "name": reference.reference_name,
                                        "create_date": str(reference.create_date), "update_date": str(reference.update_date)})
            return {"references": references_list}, 200

        return {
            "message": "There are no references present in the system!"
            }


class SingleReference(Resource):

    def get(self, _id):
        reference = ReferenceModel.find_by_id(_id)

        if reference:
            return {"id": reference.id, "name": reference.reference_name, "create_date": str(reference.create_date),
                    "update_date": str(reference.update_date)}
        return {
            "message": f"Reference with id {_id} is not available in the system"
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('reference_name', type=str, required=True, help="This is a mandatory field!")

        data = parser.parse_args()

        if ReferenceModel.find_by_name(data['reference_name']):
            return {"message": f"Reference {data['reference_name']} is already present in the system!"}, 401

        new_reference = ReferenceModel(None, data['reference_name'],  dt.now(), None)
        new_reference.save_to_database()

        new_reference_added = ReferenceModel.find_by_name(data['reference_name'])

        return {"id": new_reference_added.id, "mode_name": new_reference_added.reference_name,
                "create_date": str(new_reference_added.create_date), "update_date": new_reference_added.update_date}

    def delete(self, _id):
        reference = ReferenceModel.find_by_id(_id)
        if reference:
            deleted_reference_name = reference.reference_name
            reference.remove_from_database()
            return {"message": f"{deleted_reference_name} Reference has been deleted from the system!"}, 201

        return {
            "message": "Reference not present in the system!"
        }
