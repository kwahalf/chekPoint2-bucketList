from flask_restplus import Resource
from flask import abort, request
from app.bucketlist_api.endpoints.serializers import bucket_list, api, bucket_input, edit_bucket_item, bucket_item, bucket
from app.bucketlist_api.endpoints.persers import pagination_and_search_arguments
from app.bucketlist_api.models import User, Bucketlist, BucketItem


ns = api.namespace('bucketlists', description='Bucketlist related operations')
api.add_namespace(ns)


@ns.route('/')
@api.response(401, 'user is not legit')
class Bucketlists(Resource):
    """this class handles the creation and retrival of bucketlists"""
    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(201, 'bucketlist sucessfully created')
    @api.expect(bucket_input)
    @api.marshal_list_with(bucket)
    def post(self):
        """Handle POST request for this resource. Url ---> /bucketlists/"""
        # Get the access token from the header
        access_token = request.headers.get('Authorization')
        post_data = request.json
        if access_token:
                # Attempt to decode the token and get the User ID
                user_id = User.decode_token(access_token)
                if not isinstance(user_id, str):
                    name = post_data['name']
                    bucketlist = Bucketlist(name=name, created_by = user_id)
                    bucketlist.save()
                    return bucketlist, 201
                abort(401, user_id)
    

    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(200, 'bucketlists found')
    @api.response(404, 'bucketlist not found')
    @api.marshal_list_with(bucket_list)
    @api.expect(pagination_and_search_arguments, validate=True)
    def get(self):
        """Handle GET request for this resource. Url ---> /bucketlists/"""
        # Get the access token from the header
        access_token = request.headers.get('Authorization')
        if access_token:
            # Attempt to decode the token and get the User ID
                user_id = User.decode_token(access_token)
                bucketlists = Bucketlist.query.filter_by(created_by=user_id)
                if not isinstance(user_id, str):
                    # Go ahead and handle the request, the user is authenticated
                    # GET all the bucketlists created by this user
                    args = pagination_and_search_arguments.parse_args(request)
                    page = args.get('page', 1)
                    per_page = args.get('per_page', 10)
                    q = args.get('q')
                    if q:
                        bucketlists = Bucketlist.query.filter_by(created_by=user_id).filter(Bucketlist.name.ilike('%'+q+'%')).paginate(page, per_page, False)
                    else:
                        bucketlists = Bucketlist.query.filter_by(created_by=user_id).paginate(page, per_page, False)
                    results = []
                    if not bucketlists:
                        # There is no bucketlist with this ID for this User, so
                        # Raise an HTTPException with a 404 not found status code
                        abort(404)
                    for bucketlist in bucketlists.items:
                        bucketitems = BucketItem.query.filter_by(bucket_id=bucketlist.id)
                        items = [item for item in bucketitems]
                        bucket = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'items': items,
                        'date_created': bucketlist.date_created ,
                        'date_modified': bucketlist.date_modified ,
                        'created_by': bucketlist.created_by,
                        }
                        results.append(bucket)
                    return results, 200
        abort(401, user_id)


@ns.route('/<int:id>')
@api.response(401, 'user is not legit')
class BucketlistsManipulation(Resource):
    """This class handles the deletion, updating and retrival of a
        bucketlist by ID"""

    @api.header('Authorization', 'JWT Token', required=True)
    def delete(self, id):
        """Handle DELETE request for this resource. 
            Url ---> /bucketlists/<id>"""
        # get the access token from the authorization header
        access_token = request.headers.get('Authorization')

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                bucketlist = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                # delete the bucketlist using our delete method
                bucketlist.delete()
                return {
                    "message": "bucketlist {} deleted".format(bucketlist.id)
                }, 200
        abort(401, user_id)

    @api.response(404, 'bucketlist not found')
    @api.response(200, 'bucketlists successfuly updated')
    @api.marshal_with(bucket)
    @api.expect(bucket_input)
    @api.header('Authorization', 'JWT Token', required=True)
    def put(self, id):
        """Handle PUT request for this resource. 
            Url ---> /bucketlists/<id>"""
        # get the access token from the authorization header
        access_token = request.headers.get('Authorization')

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                bucketlist = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                # Obtain the new name of the bucketlist from the request data
                name = request.json['name']

                bucketlist.name = name
                bucketlist.save()
                return bucketlist, 200
        abort(401, user_id)


    @api.response(404, 'bucketlist not found')
    @api.response(200, 'bucketlists found')
    @api.header('Authorization', 'JWT Token', required=True)
    @api.marshal_with(bucket_list)
    def get(self, id):
        """Handle GET request for this resource. 
            Url ---> /bucketlists/<id>"""
        # get the access token from the authorization header
        access_token = request.headers.get('Authorization')

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from 
                # the URL (<int:id>)
                bucketlist = Bucketlist.query.filter_by(id=id, created_by=user_id).first()
                if not bucketlist:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                # Handle GET request, sending back the bucketlist to the user
                bucketitems = BucketItem.query.filter_by(bucket_id=bucketlist.id)
                items = [item for item in bucketitems]
                bucket = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'items': items,
                        'date_created': bucketlist.date_created ,
                        'date_modified': bucketlist.date_modified ,
                        'created_by': bucketlist.created_by,
                        }
                return bucket, 200
        abort(401, user_id)


@ns.route('/<int:id>/items/')
@api.response(401, 'user is not legit')
class Bucketitems(Resource):
    """This class handles the creation of bucketitems"""
    @api.header('Authorization', 'JWT Token', required=True)
    @api.response(201, 'bucketitem sucessfully created')
    @api.marshal_with(bucket_item, code=201)
    @api.expect(bucket_input)
    def post(self, id):
        """Handle POST request for this resource. 
            Url ---> /bucketlists/<id>/items/"""
        # Get the access token from the header
        access_token = request.headers.get('Authorization')
        post_data = request.json
        if access_token:
                # Attempt to decode the token and get the User ID
                user_id = User.decode_token(access_token)
                #use = User.query.filter_by(id=user_id).first()
                if not isinstance(user_id, str):
                    name = post_data['name']
                    bucketitem = BucketItem(name=name, bucket_id=id)
                    bucketitem.save()
                    return bucketitem, 201
                abort(401, user_id) 

@ns.route('/<int:id>/items/<int:item_id>')
@api.response(401, 'user is not legit')
class BucketItemManipulation(Resource):
    """This class handles the deletetion and update of a bucketitem by ID"""

    @api.response(404, 'bucketitem not found')
    @api.header('Authorization', 'JWT Token', required=True)
    def delete(self, id, item_id):
        """Handle POST request for this resource. 
            Url ---> /bucketlists/<id>/items/"""
        # get the access token from the authorization header
        access_token = request.headers.get('Authorization')

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                bucketitem = BucketItem.query.filter_by(id=item_id, bucket_id=id).first()
                if not bucketitem:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                # delete the bucketlist using our delete method
                bucketitem.delete()
                return {
                    "message": "bucketitem {} deleted".format(bucketitem.id)
                }, 200
        abort(401, user_id)

    @api.response(404, 'bucketitem not found')
    @api.response(200, 'bucketitem successfuly updated')
    @api.expect(edit_bucket_item)
    @api.marshal_with(bucket_item)
    @api.header('Authorization', 'JWT Token', required=True)
    def put(self, id, item_id):
        """Handle POST request for this resource. 
            Url ---> /bucketlists/<id>/items/"""
        # get the access token from the authorization header
        access_token = request.headers.get('Authorization')

        if access_token:
            # Get the user id related to this access token
            user_id = User.decode_token(access_token)

            if not isinstance(user_id, str):
                # If the id is not a string(error), we have a user id
                # Get the bucketlist with the id specified from the URL (<int:id>)
                bucketitem = BucketItem.query.filter_by(id=item_id, bucket_id=id).first()
                if not bucketitem:
                    # There is no bucketlist with this ID for this User, so
                    # Raise an HTTPException with a 404 not found status code
                    abort(404)

                # Obtain the new name of the bucketlist from the request data
                name = request.json['name']
                done = request.json['done']

                bucketitem.name = name
                bucketitem.done = done
                bucketitem.save()
                return bucketitem, 200
        abort(401, user_id)
