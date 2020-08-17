from flask import make_response, render_template
from werkzeug.datastructures import MultiDict
from flask_restful import request, Resource
from datetime import datetime as dt

from ...models.donations.DonationsModel import DonationsModel
from ...models.donations.KindDonationsModel import KindDonationsModel
from ...models.donations.ChequeDonationsModel import ChequeDonationsModel
from ...models.donations.OnlineDonationsModel import OnlineDonationsModel
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


class ShowDonationsForm(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template("./donations/forms/add_donation.html",
                                             title="Add a Donation",),
                             200, headers)


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
        donation_title = ""
        date_of_donation = ""
        donation_mode_id = 0
        project_id = 0
        donor_id = 0
        amount_in_figures = 0
        amount_in_words = ""
        cheque_number = 0
        donor_bank = 0
        date_on_cheque = ""
        date_of_cheque_donation_credit = ""
        date_of_online_donation_initiation = ""
        date_of_online_donation_credit = ""
        online_donation_transaction_id = ""

        if request.method == "POST":
            donation_title = request.form.get("donation_title")
            date_of_donation = request.form.get("date_of_donation")
            donation_mode_id = request.form.get("donation_mode_id")
            project_id = request.form.get("project_id")
            donor_id = request.form.get("donor_id")
            amount_in_figures = request.form.get("amount_in_figures")
            amount_in_words = request.form.get("amount_in_words")

            if MM.find_by_id(donation_mode_id) == "Online":
                date_of_online_donation_initiation = request.form.get("date_of_donation")
                date_of_online_donation_credit = request.form.get("date_of_credit")
                online_donation_transaction_id = request.form.get("transaction_id")

                new_online_donation = OnlineDonationModel(
                    None,
                    date_of_online_donation_initiation,
                    date_of_online_donation_credit,
                    online_donation_transaction_id,
                    dt.now()
                )
                new_online_donation.save_to_database()

            elif MM.find_by_id(donation_mode_id) == "Cheque":
                cheque_number = request.form.get("cheque_number")
                donor_bank = request.form.get("donor_bank")
                date_on_cheque = request.form.get("date_on_cheque")
                date_of_cheque_donation_credit = request.form.get("date_of_credit")

            elif MM.find_by_id(donation_mode_id) == "Kind":
                pass

            else:
                pass

        donation_date = dt.date(dt.strptime(date_of_donation, "%Y-%m-%d"))

        new_donation = DonationsModel(
            None,
            donation_title,
            donation_date,
            donation_mode_id,
            donor_id,
            project_id,
            dt.now()
        )

        new_donation.save_to_database()
        donation_added = DonationsModel.find_by_title(donation_title)

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
