from flask_restful import Resource, request
from flask import make_response, render_template
from datetime import datetime as dt

from dms.models.donors.DonorsModel import DonorsModel


class Donors(Resource):
    def get(self):
        donors = DonorsModel.get_all_donors()
        donors_list = []

        # TODO Use LIST Comprehension for returning the donors
        if donors:
            for donor in donors:
                donors_list.append(
                    {
                        "id": donor.id,
                        "name": donor.state_name,
                        "email_address": donor.email_address,
                        "gender": donor.gender,
                        "date_of_birth": donor.date_of_birth,
                        "date_of_anniversary": donor.date_of_anniversary,
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
                        "update_date": str(donor.update_date),
                    }
                )

            return {"donors": donors_list}, 200

        return {"message": "No Donors available in the system!"}, 404


class ShowDonorsForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('./donors/forms/donor-registration-form.html',
                                             title="Donor Registration Form"),
                             200, headers)


class SingleDonor(Resource):
    def get(self, _id):
        donor = DonorsModel.find_by_name(_id)

        if donor:
            return (
                {
                    "id": donor.id,
                    "name": donor.name,
                    "email_address": donor.email_address,
                    "gender": donor.gender,
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
                    "update_date": str(donor.update_date),
                },
                200,
            )

        return {"message": f"No donor with id {_id} available in the system!"}, 404

    def post(self):
        name = ""
        email_address = ""
        gender = ""
        date_f_birth = ""
        date_of_anniversary = ""
        pan = ""
        uid = ""
        country_code = ""
        phone_number = ""
        reference_id = 0
        referrer_name = ""
        other_reference = ""
        address_line_1 = ""
        address_line_2 = ""
        city = ""
        state = ""
        country = ""
        pincode = ""

        if request.method == "POST":
            
        parser.add_argument(
            "name",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "email_address",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "gender",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "date_of_birth",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "date_of_anniversary",
            type=str,
            required=True,
            help="This is mandatory field to be filled",
        )
        parser.add_argument(
            "pan",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "uid",
            type=int,
            required=True,
            help="This is a mandatory value to be filled",
        )
        parser.add_argument(
            "country_code",
            type=int,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "phone_number",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "reference",
            type=int,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "other_reference",
            type=str,
            required=False,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "referrer_name",
            type=str,
            required=False,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "address_line_1",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "address_line_2",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "city",
            type=str,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "state",
            type=int,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "country",
            type=int,
            required=True,
            help="This is a mandatory field to be filled",
        )
        parser.add_argument(
            "pincode",
            type=int,
            required=True,
            help="This is a mandatory field to be filled",
        )

        data = parser.parse_args()

        # To convert the date received in string format from json request to DATE format
        date_of_birth = dt.strptime(data["date_of_birth"], "%Y-%m-%d")
        date_of_anniversary = dt.strptime(data["date_of_anniversary"], "%Y-%m-%d")

        if DonorsModel.find_by_name(data["name"]):
            return (
                {"message": f"Donor {data['name']} is already present in the system!"},
                400,
            )

        new_donor = DonorsModel(
            None,
            data["name"],
            data["email_address"],
            data["gender"],
            date_of_birth,
            date_of_anniversary,
            data["pan"],
            data["uid"],
            data["country_code"],
            data["phone_number"],
            data["reference"],
            data["other_reference"],
            data["referrer_name"],
            data["address_line_1"],
            data["address_line_2"],
            data["city"],
            data["state"],
            data["country"],
            data["pincode"],
            dt.now(),
            None,
        )

        new_donor.save_to_database()

        new_donor_added = DonorsModel.find_by_name(data["name"])
        return (
            {
                "id": new_donor_added.id,
                "name": new_donor_added.name,
                "email_address": new_donor_added.email_address,
                "gender": new_donor_added.gender,
                "date_of_birth": str(new_donor_added.date_of_birth),
                "date_of_anniversary": str(new_donor_added.date_of_anniversary),
                "dpan number": new_donor_added.pan,
                "UID": new_donor_added.uid,
                "country_code": new_donor_added.country_code,
                "phone_number": new_donor_added.phone_number,
                "reference_id": new_donor_added.reference_id,
                "other_reference": new_donor_added.other_reference,
                "referrer_name": new_donor_added.referrer_name,
                "address_line_1": new_donor_added.address_line_1,
                "address_line_2": new_donor_added.address_line_2,
                "city": new_donor_added.city,
                "state_id": new_donor_added.state_id,
                "country_id": new_donor_added.country_id,
                "pincode": new_donor_added.pincode,
                "create_date": str(new_donor_added.create_date),
                "update_date": str(new_donor_added.update_date),
            },
            201,
        )

    def delete(self, _id):
        donor = DonorsModel.find_by_id(_id)

        if donor:
            deleted_donor_name = donor.name
            donor.remove_from_database()
            return (
                {
                    "message": f"Donor {deleted_donor_name} was successfully deleted from system!"
                },
                204,
            )

        return {"message": f"Donor with id {_id} is not available in the system!"}, 400

    def put(self, _id):
        donor = DonorsModel.find_by_id(_id)

        if donor:
            parser = reqparse.RequestParser()

            # parser.add_argument('name', type=str, required=True, help='This is a mandatory field to be filled')
            parser.add_argument(
                "email_address",
                type=str,
                required=False,
                help="This is a mandatory field to be filled",
            )
            # parser.add_argument('date_of_birth', type=str, required=True,
            #                     help='This is a mandatory field to be filled')
            parser.add_argument(
                "date_of_anniversary",
                type=str,
                required=False,
                help="This is mandatory field to be filled",
            )
            # parser.add_argument('pan', type=str, required=True, help='This is a mandatory field to be filled')
            # parser.add_argument('uid', type=int, required=True, help='This is a mandatory value to be filled')
            parser.add_argument(
                "country_code",
                type=int,
                required=False,
                help="This is a mandatory field to be filled",
            )
            parser.add_argument(
                "phone_number",
                type=str,
                required=False,
                help="This is a mandatory field to be filled",
            )
            # parser.add_argument('reference', type=int, required=True, help='This is a mandatory field to be filled')
            # parser.add_argument('other_reference', type=str, required=False,
            #                   help='This is a mandatory field to be filled')
            # parser.add_argument('referrer_name', type=str, required=False,
            #                    help='This is a mandatory field to be filled')
            parser.add_argument(
                "address_line_1",
                type=str,
                required=False,
                help="This is a mandatory field to be filled",
            )
            parser.add_argument(
                "address_line_2",
                type=str,
                required=False,
                help="This is a mandatory field to be filled",
            )
            parser.add_argument(
                "city",
                type=str,
                required=False,
                help="This is a mandatory field to be filled",
            )
            parser.add_argument(
                "state",
                type=int,
                required=False,
                help="This is a mandatory field  to be filled",
            )
            parser.add_argument(
                "country",
                type=int,
                required=False,
                help="This is a mandatory field to be filled",
            )
            parser.add_argument(
                "pincode",
                type=int,
                required=False,
                help="This is a mandatory field to be filled",
            )

            data = parser.parse_args()

            donor.email_address = data["email_address"]
            donor.date_of_anniversary = dt.strptime(
                data["date_of_anniversary"], "%Y-%m-%d"
            )
            donor.country_code = data["country_code"]
            donor.phone_number = data["phone_number"]
            donor.address_line_1 = data["address_line_1"]
            donor.address_line_1 = data["address_line_2"]
            donor.city = data["city"]
            donor.state = data["state"]
            data.country = data["country"]
            data.pincode = data["pincode"]
            donor.update_date = dt.now()

            DonorsModel.commit_to_database()

            updated_donor = DonorsModel.find_by_id(_id)
            return (
                {
                    "id": updated_donor.id,
                    "name": updated_donor.name,
                    "email_address": updated_donor.email_address,
                    "gender": updated_donor.gender,
                    "date_of_birth": str(updated_donor.date_of_birth),
                    "date_of_anniversary": str(updated_donor.date_of_anniversary),
                    "dpan number": updated_donor.pan,
                    "UID": updated_donor.uid,
                    "country_code": updated_donor.country_code,
                    "phone_number": updated_donor.phone_number,
                    "reference_id": updated_donor.reference_id,
                    "other_reference": updated_donor.other_reference,
                    "referrer_name": updated_donor.referrer_name,
                    "address_line_1": updated_donor.address_line_1,
                    "address_line_2": updated_donor.address_line_2,
                    "city": updated_donor.city,
                    "state_id": updated_donor.state_id,
                    "country_id": updated_donor.country_id,
                    "pincode": updated_donor.pincode,
                    "create_date": str(updated_donor.create_date),
                    "update_date": str(updated_donor.update_date),
                },
                201,
            )
