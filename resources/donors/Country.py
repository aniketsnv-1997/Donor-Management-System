from flask_restful import reqparse, Resource
from datetime import datetime as dt

from models.donors.CountryModel import CountryModel


class Country(Resource):

    def get(self):
        countries = CountryModel.get_all_country()
        country_list = []

        # TODO Use LIST Comprehension for returning the Countries

        for country in countries:
            country_list.append(
                {"id": country.id, "name": country.country_name, "country_id": country.country_id,
                 "create_date": str(country.create_date), "update_date": str(country.update_date)})

        return {"country": country_list}, 200


class SingleCountry(Resource):

    def get(self, name):
        country = CountryModel.find_by_name(name)

        return {"id": country.id, "name": country.country_name, "country_id": country.country_id,
                "create_date": str(country.create_date), "update_date": str(country.update_date)}, 200

    def post(self, name):
        parser = reqparse.RequestParser()

        parser.add_argument('country_id', type=int, required=True, help='This is a mandatory field to be filled')
        data = parser.parse_args()

        if CountryModel.find_by_name(name):
            return {"message": f"Country with name {name} is already present in the system!"}, 401

        new_country = CountryModel(None, name, data['country_id'], dt.date(dt.now()), None)
        new_country.save_to_database()
        return SingleCountry.get(self, name), 201

    def delete(self, name):
        country = CountryModel.find_by_name(name)
        if country is None:
            return {"message": f"Country with name {name} is not present in the system!"}, 401

        country.remove_from_database()

        return 204

    def put(self, name):
        pass
