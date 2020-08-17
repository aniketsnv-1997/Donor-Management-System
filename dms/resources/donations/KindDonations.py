from flask_restful import reqparse, Resource
from datetime import datetime as dt

from dms.models.donations.KindDonationsModel import KindDonationsModel
from dms.models.donations.DonationsModel import DonationsModel


class KindDonations(Resource):
    def get(self):
        kind_donations = KindDonationModel.get_all_kind_donations()
        kind_donations_list = []

        if kind_donations_list:
            for kind_donation in kind_donations:
                kind_donations_list.append(
                    {
                        "id": kind_donation.id,
                        "item": kind_donation.item,
                        "quantity": kind_donation.quantity,
                        "unit": kind_donation.unit,
                        "donation_id": kind_donation.donation_id,
                        "create_date": kind_donation.create_date,
                    }
                )
                return {"kind_donations": kind_donations_list}, 200

        return {"message": "No kind donations found in database"}, 404


class SingleKindDonation(Resource):
    def get(self, _id):

        single_kind_donation = KindDonationModel.find_by_id(_id)
        if single_kind_donation:
            return (
                {
                    "id": single_kind_donation.id,
                    "item": single_kind_donation.item,
                    "quantity": single_kind_donation.quantity,
                    "unit": single_kind_donation.unit,
                    "donation_id": single_kind_donation.donation_id,
                    "create_date": single_kind_donation.create_date,
                },
                200,
            )

        return {"message": "No single donation with a given id found"}, 404
