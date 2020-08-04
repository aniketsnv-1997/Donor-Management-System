from flask_restful import reqparse, Resource
from flask import make_response, render_template, request
from datetime import datetime as dt

from dms.models.donors.ReferencesModel import ReferenceModel


class Reference(Resource):
    def get(self):
        references = ReferenceModel.get_all_references()
        references_list = []

        # TODO Use LIST Comprehension for returning the references
        if references:
            for reference in references:
                references_list.append(
                    {
                        "id": reference.id,
                        "name": reference.reference_name,
                        "create_date": str(reference.create_date),
                        "update_date": str(reference.update_date),
                    }
                )

            return {"references": references_list}, 200

        return {"message": "There are no references present in the system!"}, 404


class ShowReferenceForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("./donors/forms/add_references.html", title="Add Reference"), 200, headers)


class SingleReference(Resource):
    def get(self, _id):
        reference = ReferenceModel.find_by_id(_id)

        if reference:
            return (
                {
                    "id": reference.id,
                    "name": reference.reference_name,
                    "create_date": str(reference.create_date),
                    "update_date": str(reference.update_date),
                },
                200,
            )

        return (
            {"message": f"Reference with id {_id} is not available in the system"},
            404,
        )

    def post(self):
        reference_name = ""

        if request.method == "POST":
            reference_name = request.form.get("reference_name")

        if ReferenceModel.find_by_name(reference_name):
            return (
                {
                    "message": f"Reference {reference_name} is already present in the system!"
                },
                400,
            )

        new_reference = ReferenceModel(None, reference_name, dt.now(), None)
        new_reference.save_to_database()

        new_reference_added = ReferenceModel.find_by_name(reference_name)

        return (
            {
                "id": new_reference_added.id,
                "mode_name": new_reference_added.reference_name,
                "create_date": str(new_reference_added.create_date),
                "update_date": str(new_reference_added.update_date),
            },
            201,
        )

    def delete(self, _id):
        reference = ReferenceModel.find_by_id(_id)
        if reference:
            deleted_reference_name = reference.reference_name
            reference.remove_from_database()
            return (
                {
                    "message": f"{deleted_reference_name} Reference has been deleted from the system!"
                },
                201,
            )

        return {"message": "Reference not present in the system!"}, 400
