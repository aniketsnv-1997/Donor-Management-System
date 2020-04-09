from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.donors.ReferencesModel import ReferenceModel


class Reference(Resource):

    def get(self):
        references = ReferenceModel.get_all_references()
        references_list = []

        # TODO Use LIST Comprehension for returning the references

        for reference in references:
            references_list.append({"id": reference.id, "name": reference.reference_name,
                                    "create_date": str(reference.create_date), "update_date": str(reference.update_date)})

        return {"references": references_list}, 200


class SingleReference(Resource):

    def get(self, name):
        reference = ReferenceModel.find_by_name(name)

        return {"id": reference.id, "name": reference.reference_name, "create_date": str(reference.create_date),
                "update_date": str(reference.update_date)}

    def post(self, name):
        parser = reqparse.RequestParser()

        if ReferenceModel.find_by_name(name):
            return {"message": f"Reference with name {name} is already present in the system!"}, 401

        new_reference = ReferenceModel(None, name,  dt.date(dt.now()), None)
        new_reference.save_to_database()
        return SingleReference.get(self, name), 201

    def delete(self, name):
        reference = ReferenceModel.find_by_name(name)
        if reference is None:
            return {"message": f"Reference with name {name} is not present in the system!"}, 401

        reference.remove_from_database()

        return 204

    def put(self, name):
        pass
