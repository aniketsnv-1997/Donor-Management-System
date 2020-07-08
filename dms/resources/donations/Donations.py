from werkzeug.datastructures import MultiDict
from flask_restful import reqparse, Resource
from datetime import datetime as dt

from ...models.donations.DonationsModel import DonationsModel
from ...models.donations.KindDonationsModel import KindDonationModel
from ...models.donations.ChequeDonationsModel import ChequeDonationsModel
from ...models.donations.ModesModel import MM


class Donation(Resource):
    def get(self):

        donations = DonationsModel.get_all_donations()
        donations_list = []

        if donations:
            for donation in donations:
                donations_list.append(
                    {
                        "id": donation.id,
                        "title": donation.donation_title,
                        "date_of_donation": str(donation.date_of_donation),
                        "mode_id": donation.mode_id,
                        "amount_in_figures": donation.amount_in_figures,
                        "amount_in_words": donation.amount_in_words,
                        "cheque_number": donation.cheque_number,
                        "cheque_date": str(donation.cheque_date),
                        "donor_bank": donation.donor_bank,
                        "donor_id": donation.donation_id,
                        "project_id": donation.project_id,
                    }
                )

            return {"donations": donations_list}, 200
        return {"message": "No donations present in the system"}, 200


class SingleDonation(Resource):
    def get(self, _id):
        donation = DonationsModel.find_by_id(_id)

        if donation:
            return (
                {
                    "id": donation.id,
                    "title": donation.donation_title,
                    "date_of_donation": str(donation.date_of_donation),
                    "mode_id": donation.mode_id,
                    "amount_in_figures": donation.amount_in_figures,
                    "amount_in_words": donation.amount_in_words,
                    "cheque_number": donation.cheque_number,
                    "cheque_date": str(donation.cheque_date),
                    "donor_bank": donation.donor_bank,
                    "donor_id": donation.donation_id,
                    "project_id": donation.project_id,
                },
                200,
            )

        return (
            {"message": f"Donation with id {_id} is not available in the system"},
            404,
        )

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument(
            "donation_title", type=str, required=True, help="This is a mandatory field"
        )

        parser.add_argument(
            "date_of_donation", type=str, required=False, help="This is a mandatory field"
        )

        parser.add_argument(
            "mode_id", type=int, required=True, help="This is a mandatory field"
        )

        parser.add_argument(
            "donor_id", type=int, required=True, help="This is a mandatory field"
        )
        parser.add_argument(
            "project_id", type=int, required=False, help="This is a mandatory field"
        )

        general_donation_data = parser.parse_args()
        donation_date = dt.date(dt.strptime(general_donation_data["date_of_donation"], "%Y-%m-%d"))
        new_donation = DonationsModel(
            None,
            general_donation_data["donation_title"],
            donation_date,
            general_donation_data["mode_id"],
            general_donation_data['donor_id'],
            general_donation_data['project_id'],
            dt.now()
        )

        new_donation.save_to_database()
        donation_added = DonationsModel.find_by_title(general_donation_data['donation_title'])

        if MM.find_mode_name_by_id(donation_added.mode_id) == "Kind":
            print("Donation is in Kind format")

        elif MM.find_mode_name_by_id(general_donation_data['mode_id']) == 'Cash':
            parser.add_argument(
                "amount_in_figures",
                type=int,
                required=True,
                help="This is a mandatory field",
            )
            parser.add_argument(
                "amount_in_words", type=str, required=True, help="This is a mandatory field"
            )

        elif MM.find_mode_name_by_id(donation_added.mode_id) == "Cheque":
            parser.add_argument(
                "amount_in_figures",
                type=int,
                required=True,
                help="This is a mandatory field",
            )
            parser.add_argument(
                "amount_in_words", type=str, required=True, help="This is a mandatory field"
            )
            parser.add_argument(
                "cheque_number", type=str, required=True, help="This is a mandatory field"
            )
            parser.add_argument(
                "cheque_date", type=str, required=False, help="This is a mandatory field"
            )

            parser.add_argument(
                "date_of_credit", type=str, required=False, help="This is a mandatory field"
            )

            parser.add_argument(
                "donor_bank", type=str, required=True, help="This is a mandatory field"
            )

            cheque_donation_details = parser.parse_args()
            cheque_date = dt.date(dt.strptime(cheque_donation_details["cheque_date"], "%Y-%m-%d"))
            credit_date = dt.date(dt.strptime(cheque_donation_details["date_of_credit"], "%Y-%m-%d"))

            new_cheque_donation = ChequeDonationsModel(None, cheque_donation_details['cheque_number'], cheque_date,
                                                       cheque_donation_details['amount_in_figures'], cheque_donation_details['amount_in_words'],
                                                       credit_date, cheque_donation_details['donor_bank'], donation_added.id, dt.now())
            new_cheque_donation.save_to_database()

    def delete(self, _id):
        donation = DonationsModel.find_by_id(_id)
        if donation:
            deleted_donation_id = donation.id

            kind_donations_related_to_deleted_donation = KindDonationModel.find_by_donation_id(
                deleted_donation_id
            )

            if kind_donations_related_to_deleted_donation:
                for (
                        kind_donation_tobe_deleted
                ) in kind_donations_related_to_deleted_donation:
                    kind_donation_tobe_deleted.remove_from_database()

                donation.remove_from_database()

                return {
                    "message": f"Donation with id {_id} is successfully deleted from the system. There were"
                               f"{len(kind_donations_related_to_deleted_donation)} kind donations related to the deleted"
                               f"donation, which also have been deleted successfully from the system!"
                }

            donation.remove_from_database()
            return {
                "message": f"Donation with id {_id} is successfully deleted from the system. There were no kind"
                           f"donations associated with the deleted donation"
            }

        return {"message": "No such donation present in the system!"}
