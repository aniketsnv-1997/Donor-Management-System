from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.donors.DonorsModel import DonorsModel


class Donors(Resource):

    def get(self):
        donors = DonorsModel.get_all_donors()
        donors_list = []

        # TODO Use LIST Comprehension for returning the donors
        if donors:
            for donor in donors:
                donors_list.append({"id": donor.id, "name": donor.state_name, "email_address": donor.email_address,
                                    "date_of_birth": donor.date_of_birth, "date_of_anniversary": donor.date_of_anniversary,
                                    "pan": donor.pan, "uid": donor.uid, "country_code": donor.country_code,
                                    "phone_number": donor.phone_number, "reference": donor.reference,
                                    "reference": donor.reference, "other_reference": donor.other_reference,
                                    "referrer_name": donor.referrer_name, "address_line_1": donor.address_line_1,
                                    "address_line_2": donor.address_line_2, "city": donor.city, "state": donor.state,
                                    "country": donor.country, "pincode": donor.pincode, "create_date": str(donor.create_date),
                                    "update_date": str(donor.update_date)})

            return {"donors": donors_list}, 200

        return {
            "message": "No Donors available in the system!"
        }, 401


class SingleDonor(Resource):

    def get(self, _id):
        donor = DonorsModel.find_by_name(_id)

        if donor:
            return {
                "id": donor.id,
                "name": donor.name,
                "email_address": donor.email_address,
                "date_of_birth": str(donor.date_of_birth),
                "date_of_anniversary": str(donor.date_of_anniversary),
                "pan": donor.pan,
                "uid": donor.uid,
                "country_code": donor.country_code,
                "phone_number": donor.phone_number,
                "reference": donor.reference,
                "other_reference": donor.other_reference,
                "referrer_name": donor.referrer_name,
                "address_line_1": donor.address_line_1,
                "address_line_2": donor.address_line_2,
                "city": donor.city,
                "state": donor.state,
                "country": donor.country,
                "pincode": donor.pincode,
                "create_date": str(donor.create_date),
                "update_date": str(donor.update_date)
            }, 200

        return {
            "message": f"No donor with id {_id} available in the system!"
        }, 401

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('name', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('email_address', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('date_of_birth', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('date_of_anniversary', type=str, required=True, help='This is mandatory field to be filled')
        parser.add_argument('pan', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('uid', type=int, required=True, help='This is a mandatory value to be filled')
        parser.add_argument('country_code', type=int, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('phone_number', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('reference', type=int, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('other_reference', type=str, required=False, help='This is a mandatory field to be filled')
        parser.add_argument('referrer_name', type=str, required=False, help='This is a mandatory field to be filled')
        parser.add_argument('address_line_1', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('address_line_2', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('city', type=str, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('state', type=int, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('country', type=int, required=True, help='This is a mandatory field to be filled')
        parser.add_argument('pincode', type=int, required=True, help='This is a mandatory field to be filled')

        data = parser.parse_args()

        # To convert the date received in string format from json request to DATE format
        date_of_birth = dt.strptime(data['date_of_birth'], '%Y-%m-%d')
        date_of_anniversary = dt.strptime(data['date_of_anniversary'], '%Y-%m-%d')

        if DonorsModel.find_by_name(data['name']):
            return {
                "message": f"Donor {data['name']} is already present in the system!"
                }, 401

        new_donor = DonorsModel(
            None,
            data['name'],
            data['email_address'],
            date_of_birth,
            date_of_anniversary,
            data['pan'],
            data['uid'],
            data['country_code'],
            data['phone_number'],
            data['reference'],
            data['other_reference'],
            data['referrer_name'],
            data['address_line_1'],
            data['address_line_2'],
            data['city'],
            data['state'],
            data['country'],
            data['pincode'],
            dt.now(),
            None
        )

        new_donor.save_to_database()

        new_donor_added = DonorsModel.find_by_name(data['name'])
        return {
            None,
            new_donor_added.id,
            new_donor_added.email_address,
            new_donor_added.date_of_birth,
            new_donor_added.date_of_anniversary,
            new_donor_added.pan,
            new_donor_added.uid,
            new_donor_added.country_id,
            new_donor_added.phone_number,
            new_donor_added.reference_id,
            new_donor_added.other_reference,
            new_donor_added.referrer_name,
            new_donor_added.address_line_1,
            new_donor_added.address_line_2,
            new_donor_added.city,
            new_donor_added.state_id,
            new_donor_added.country_id,
            new_donor_added.pincode,
            dt.now(),
            None
        }, 201

    def delete(self, _id):
        donor = DonorsModel.find_by_id(_id)

        if donor:
            deleted_country = donor.name
            donor.remove_from_database()
            return {
                "message": f"Donor {donor.name} was successfully deleted from system!"
            }, 204

        return {
            "message": f"Donor with id {_id} is not available in the system!"
        }, 401

    def put(self, _id):
        donor = DonorsModel.find_by_id(_id)

        if donor:
            parser = reqparse.RequestParser()

            # parser.add_argument('name', type=str, required=True, help='This is a mandatory field to be filled')
            parser.add_argument('email_address', type=str, required=True,
                                 help='This is a mandatory field to be filled')
            # parser.add_argument('date_of_birth', type=str, required=True,
            #                     help='This is a mandatory field to be filled')
            parser.add_argument('date_of_anniversary', type=str, required=True,
                                help='This is mandatory field to be filled')
            # parser.add_argument('pan', type=str, required=True, help='This is a mandatory field to be filled')
            # parser.add_argument('uid', type=int, required=True, help='This is a mandatory value to be filled')
            parser.add_argument('country_code', type=int, required=True, help='This is a mandatory field to be filled')
            parser.add_argument('phone_number', type=str, required=True, help='This is a mandatory field to be filled')
            # parser.add_argument('reference', type=int, required=True, help='This is a mandatory field to be filled')
            # parser.add_argument('other_reference', type=str, required=False,
            #                   help='This is a mandatory field to be filled')
            # parser.add_argument('referrer_name', type=str, required=False,
            #                    help='This is a mandatory field to be filled')
            parser.add_argument('address_line_1', type=str, required=True,
                                help='This is a mandatory field to be filled')
            parser.add_argument('address_line_2', type=str, required=True,
                                help='This is a mandatory field to be filled')
            parser.add_argument('city', type=str, required=True, help='This is a mandatory field to be filled')
            parser.add_argument('state', type=int, required=True, help='This is a mandatory field  to be filled')
            parser.add_argument('country', type=int, required=True, help='This is a mandatory field to be filled')
            parser.add_argument('pincode', type=int, required=True, help='This is a mandatory field to be filled')

            data = parser.parse_args()

            donor.