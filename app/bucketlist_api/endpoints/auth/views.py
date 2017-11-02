
from flask_restplus import Resource
from flask import request, jsonify
from app.bucketlist_api.models import User
#from app import api
from ..serializers import profile, api

ns = api.namespace('auth', description='Operations related to user authentication')

# Define the path for the registration url --->  /auth/register
@ns.route('/register')
@api.response(401, 'error occured during registration')
@api.response(409, 'user already exists')
class Registration(Resource):
    """This class registers a new user."""
    
    @api.expect(profile)
    @api.response(201,'user registerd')
    def post(self):
        """Handle POST request for this resource. Url ---> /auth/register"""

        # Query to see if the user already exists
        post_data=request.json
        email = post_data.get('email')
        password = post_data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user:
            # There is no user so we'll try to register them
            try:
                # Register the user
                user = User(email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return response, 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return response, 401
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

            return response, 409

@ns.route('/login')
@api.response(401, 'Invalid email or password')
@api.response(500, 'Internal server error')
class Login(Resource):
    """This class-based view handles user login and access token generation."""

    @api.expect(profile)
    @api.response(200, 'logged in sucessfully')
    def post(self):
        """Handle POST request for this view. Url ---> /auth/login"""
        try:
            # Get the user object using their email (unique to every user)
            post_data=request.json
            email = post_data.get('email')
            password = post_data.get('password')
            user = User.query.filter_by(email=email).first()

            # Try to authenticate the found user using their password
            if user and user.password_is_valid(password):
                # Generate the access token. This will be used as the authorization header
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return response, 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid email or password, Please try again'
                }
                return response, 401

        except Exception as e:
            # Create a response containing an string error message
            response = {
                'message': str(e)
            }
            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return response, 500
