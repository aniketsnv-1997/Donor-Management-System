from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from dms.models.users.UsersModel import UsersModel


# Create a User Login Resource to to implement the authentication endpoint
class UserLogin(Resource):
    """
    This class is used to implement the functionality which was masked by the Flask-JWT library.
    The basic authentication and identity functions implemented under flask-JWT will be implemented from scratch in the
    class
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email_address', type=str, required=True, help='This is a mandatory field')
        parser.add_argument('password', type=str, required=True, help='This is a mandatory field')

        # 1. Will get the data from Parser
        data = parser.parse_args()

        # 2. find the user in db as per the email_Address
        user = UsersModel.find_by_email_address(data['email_address'])

        # 3. if there exists a user for the given email address, match the password of the found user
        if user and safe_str_cmp(user.password, data['password']):
            # 4. create an access token
            access_token = create_access_token(identity=user.id, fresh=True)

            # 5. create a refresh token
            refresh_token = create_refresh_token(identity=user.id)

            return {
                       "access_token": access_token,
                       "refresh_token": refresh_token,
                   }, 200

        return {"message": "Invalid credentials"}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
