from flask_restful import reqparse, Resource, request
from datetime import datetime as dt

from models.donations.DonationsModel import DonationsModel
from models.donations.KindDonationsModel import KindDonationModel


class Donation(Resource):

    def get(self):
        donations = DonationsModel.get_all_donations()
        donations_list = []

        for donation in donations:
            donations_list.append(
                {
                    "id": donation.id,
                    "date_of_donation": donation.date_of_donation,
                    "mode_id": donation.mode_id,
                    "amount_in_figures": donation.amount_in_figures,
                    "amount_in_words": donation.amount_in_words,
                    "cheque_number": donation.cheque_number,
                    "cheque_date": donation.cheque_date,
                    "donor_bank": donation.donor_bank,
                    "donor_id": donation.donation_id,
                    "project_id": donation.project_id
                }
            )

        return {"donations": donations_list}, 200


class SingleDonation(Resource):

    def get(self, _id):
        donation = DonationsModel.find_by_id(_id)

        if donation:
            return {
                       "id": donation.id,
                       "date_of_donation": donation.date_of_donation,
                       "mode_id": donation.mode_id,
                       "amount_in_figures": donation.amount_in_figures,
                       "amount_in_words": donation.amount_in_words,
                       "cheque_number": donation.cheque_number,
                       "cheque_date": donation.cheque_date,
                       "donor_bank": donation.donor_bank,
                       "donor_id": donation.donation_id,
                       "project_id": donation.project_id
                   }, 200

        return {"message": "No donation found!"}, 404

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("mode_id", type=int, required=True, help="This is a mandatory field")
        parser.add_argument("amount_in_figured", type=int, required=True, help="This is a mandatory field")
        parser.add_argument("amount_in_words", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("cheque_number", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("cheque_date", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("donor_bank", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("donor_id", type=int, required=True, help="This is a mandatory field")
        parser.add_argument("project_id", type=int, required=True, help="This is a mandatory field")

        data = parser.parse_args()

        cheque_date = dt.strptime(data['cheque_date'], '%Y-%m-%d')

        new_donation = DonationsModel(
            None,
            dt.date(dt.now()),
            data['mode_id'],
            data['amount_in_figured'],
            data['amount_in_words'],
            data['cheque_number'],
            cheque_date,
            data['donor_bank'],
            data['project_id'],
            data['donor_id']
        )

        new_donation.save_to_database()

        if data['mode_id'] == 1:
            print("The donation is a kind donation")

            parser.add_argument("kind_donation_list", type=list, action='append', required=True,
                                help="This is  mandatory field", location='json')

            data = parser.parse_args()

            print(data)

        return 201
