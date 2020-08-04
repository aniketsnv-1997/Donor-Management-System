from flask import render_template, make_response
from flask_restful import Resource
import pdfkit


class HomePage(Resource):
    def get(self):
        pdfkit.from_url("http://127.0.0.1:5000/users", "user.pdf")
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'), 200, headers)



