from flask import Flask, jsonify, request  # Tell Python that we want to use Flask, jsonify - to convert dictionary
# to json
from flask_restful import Resource, Api

app = Flask(__name__)  # "__name__" tells Flask that this application is running in some unique namespace
api = Api(app)
types = [
    {
        'name': 'project',
        'details': [
            {
                'description': 'A long term task to be done. May last for years',
                'example': 'SDA',
                'create_date': '24-Feb-2020'
            }
         ],
    },

    {
        'name': 'activity',
        'details': [
            {
                'description': 'A small activity, done for some short term quick impact',
                'example': 'Box of Happiness',
                'create_date': '25-Feb-2020'
            }
        ]
    }
]


# This route is the endpoint for Home Page
# It Should render a HTML page displaying the options to be done by Super User
@app.route('/')
def home_page():
    return 'Hello, Welcome to DMS!'

# POST /type: {type_name, type_description, create_date} - Create a Type of Project with name, description and create
# date
@app.route('/types', methods=['POST'])
def create_type():
    request_data = request.get_json()   # request.get_json() is used to fetch and collect the json data sent from
    # browser as request. request_data contains the json data fetched from browser

    new_type = {
        'name': request_data['name'],
        'details': {
            'description': request_data['description'],
            'example': request_data['example'],
            'create_date': request_data['create_date']

        }
    }
    types.append(new_type)
    return jsonify({'types': types})    # We return the jsonify version of the new data that was received from browser


# GET /types - Get the details of all the types
@app.route('/types', methods=['GET'])
def read_type():
    return jsonify({'types': types})  # A jsonify accepts only dictionaries, we passed a dummy key as 'types' and
    # gave a value of "types" which is a list to it


# GET /types/name - GEt the details and name of a specific type
@app.route('/types/<string:name>')
def read_type_with_name(name):
    for value in types:
        if value['name'] == name:
            return jsonify(value)

    return jsonify({'msg': f'No type with name {name} was found in the system'})


if __name__ == '__main__':
    app.run()  # Default port is 5000
