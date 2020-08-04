from flask_restful import Resource, request, reqparse
from flask import make_response, render_template
from datetime import datetime as dt

from dms.models.donors.DonorsModel import DonorsModel
from dms.models.donors.ReferencesModel import ReferenceModel


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
                                             title="Donor Registration Form",
                                             references=ReferenceModel.get_all_references()),
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
        date_of_birth = ""
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
            name = request.form.get("name")
            email_address = request.form.get("email_address")
            gender = request.form.get("gender")
            date_of_birth = request.form.get("date_of_birth")
            date_of_anniversary = request.form.get("date_of_anniversary")
            pan = request.form.get("pan")
            uid = request.form.get("aadhar")
            country_code = request.form.get("country_code")
            phone_number = request.form.get("phone_number")
            reference_id = request.form.get("reference_id")
            referrer_name = request.form.get("referrer_name")
            other_reference = request.form.get("other_reference")
            address_line_1 = request.form.get("address_line_1")
            address_line_2 = request.form.get("address_line_2")
            city = request.form.get("city")
            state = request.form.get("state")
            country = request.form.get("country")
            pincode = request.form.get("pincode")

        # To convert the date received in string format from json request to DATE format
        date_of_birth = dt.strptime(date_of_birth, "%Y-%m-%d")
        date_of_anniversary = dt.strptime(date_of_anniversary, "%Y-%m-%d")

        if DonorsModel.find_by_name(name):
            return (
                {"message": f"Donor {name} is already present in the system!"},
                400,
            )

        # Check if "referrer_name" is not NONE
        elif referrer_name is not None:
            new_donor = DonorsModel(
                None,
                name,
                email_address,
                gender,
                date_of_birth,
                date_of_anniversary,
                pan,
                uid,
                country_code,
                phone_number,
                reference_id,
                referrer_name,
                address_line_1,
                address_line_2,
                city,
                state,
                country,
                pincode,
                dt.now(),
            )

        # Check if "other_reference" is not NONE
        elif other_reference is not None:
            new_donor = DonorsModel(
                None,
                name,
                email_address,
                gender,
                date_of_birth,
                date_of_anniversary,
                pan,
                uid,
                country_code,
                phone_number,
                reference_id,
                other_reference,
                address_line_1,
                address_line_2,
                city,
                state,
                country,
                pincode,
                dt.now(),
            )

        # If both of the above conditions are False, execute this block
        else:
            new_donor = DonorsModel(
                None,
                name,
                email_address,
                gender,
                date_of_birth,
                date_of_anniversary,
                pan,
                uid,
                country_code,
                phone_number,
                reference_id,
                address_line_1,
                address_line_2,
                city,
                state,
                country,
                pincode,
                dt.now(),
            )

        new_donor.save_to_database()

        new_donor_added = DonorsModel.find_by_name(name)

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("./donations/donor-added.html",
                                             title="Donor Added Successfully!",
                                             message="The donor has been successfully added into the system",
                                             donor=new_donor_added),
                             200, headers)

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
            # donor.update_date = dt.now()

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
                    # "update_date": str(updated_donor.update_date),
                },
                201,
            )
