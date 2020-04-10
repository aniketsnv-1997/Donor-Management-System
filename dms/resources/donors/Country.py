from flask_restful import reqparse, Resource
from datetime import datetime as dt

from ...models.donors.CountryModel import CountryModel


class Country(Resource):

    def get(self):
        countries = CountryModel.get_all_country()
        country_list = []

        # TODO Use LIST Comprehension for returning the Countries

        if countries:
            for country in countries:
                country_list.append(
                    {
                        "id": country.id,
                        "name": country.country_name,
                        "create_date": str(country.create_date)
                    }
                )
            return {"country": country_list}, 200
        
        return {
            "message": "There are no countries present in the system!"
        }, 401


class SingleCountry(Resource):

    def get(self, _id):
        country = CountryModel.find_by_id(_id)

        if country:
            return {"id": country.id, "name": country.country_name,
                    "create_date": str(country.create_date), "update_date": str(country.update_date)}, 200

        return {
            "message": f"No country with id {_id} available in the system!"
        }, 401

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('country_name', type=str, required=True, help='This is a mandatory field to be filled')
        data = parser.parse_args()

        if CountryModel.find_by_name(data['country_name']):
            return {"message": f"Country {data['country_name']} is already present in the system!"}, 401

        new_country = CountryModel(None, data['country_name'], dt.now(), None)
        new_country.save_to_database()

        new_country_added = CountryModel.find_by_name(data['country_model'])
        return {
            "id": new_country_added.id,
            "country_name": new_country_added.country_name,
            "create_date": new_country_added.create_date,
            "update_date": new_country_added.update_date
        }, 201

    def delete(self, _id):
        country = CountryModel.find_by_id(_id)

        if country:
            deleted_country = country.country_name
            country.remove_from_database()
            return {
                "message": f"{deleted_country} has been successfully deleted from the system!"
            }, 204

        return {
            "message": "No such country exists in the system!"
        }, 401
