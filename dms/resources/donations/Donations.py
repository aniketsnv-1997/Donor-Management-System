from flask_restful import reqparse, Resource
from datetime import datetime as dt

from ...models.donations.DonationsModel import DonationsModel
from ...models.donations.KindDonationsModel import KindDonationModel
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
                        "project_id": donation.project_id
                    }
                )

            return {"donations": donations_list}, 200
        return {"message": "No donations present in the system"}, 200


class SingleDonation(Resource):

    def get(self, _id):
        donation = DonationsModel.find_by_id(_id)

        if donation:
            return {
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
                       "project_id": donation.project_id
                   }, 200

        return {"message": f"Donation with id {_id} is not available in the system"}, 404

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument("donation_title", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("mode_id", type=int, required=True, help="This is a mandatory field")
        parser.add_argument("amount_in_figures", type=int, required=True, help="This is a mandatory field")
        parser.add_argument("amount_in_words", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("cheque_number", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("cheque_date", type=str, required=False, help="This is a mandatory field")
        parser.add_argument("donor_bank", type=str, required=True, help="This is a mandatory field")
        parser.add_argument("donor_id", type=int, required=True, help="This is a mandatory field")
        parser.add_argument("project_id", type=int, required=True, help="This is a mandatory field")

        data = parser.parse_args()

        cheque_date = dt.date(dt.strptime(data['cheque_date'], '%Y-%m-%d'))
        print(cheque_date)
        print(type(cheque_date))

        new_donation = DonationsModel(
            None,
            data['donation_title'],
            dt.date(dt.now()),
            data['mode_id'],
            data['amount_in_figures'],
            data['amount_in_words'],
            data['cheque_number'],
            cheque_date,
            data['donor_bank'],
            data['project_id'],
            data['donor_id']
        )

        new_donation.save_to_database()

        new_donation_added = DonationsModel.find_by_title(data['donation_title'])
        kind_mode_of_donation = MM.find_by_name('Kind')

        if new_donation_added.id == kind_mode_of_donation.id:
            return {"message": "The donation is a kind donation"}

    def delete(self, _id):
        donation = DonationsModel.find_by_id(_id)
        if donation:
            deleted_donation_id = donation.id

            kind_donations_related_to_deleted_donation = KindDonationModel.find_by_donation_id(deleted_donation_id)

            if kind_donations_related_to_deleted_donation:
                for kind_donation_tobe_deleted in kind_donations_related_to_deleted_donation:
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

        return {
            "message": "No such donation present in the system!"
        }
