from flask_restplus import fields
from app import api


bucket_list_items = api.model('Bucketitems', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of an item'),
    'name': fields.String(required=True, description='item name'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.String(required=True, description='status of the item'),
})

bucket_list = api.model('Bucketlist', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of a bucketlist'),
    'name': fields.String(required=True, description='Bucketlist name'),
    'items': fields.List(fields.Nested(bucket_list_items),
                         description='Bucketlist items'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.String(required=True, description='Bucketlist owner'),
})


profile = api.model('profile', {
    'email': fields.String(required=True, description='user email adress'),
    'password': fields.String(required=True, description='user password'),
})

bucket_input = api.model('input', {
    'name': fields.String(required=True, description='name of bucketlist or bucket item'),
})

edit_bucket_item = api.model('edit', {
    'name': fields.String(required=True, description='name of bucketlist or bucket item'),
    'done': fields.Boolean(required=False, description='status of the bucketlist item'),
})

bucket_item = api.model('item', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of an item'),
    'name': fields.String(required=True, description='item name'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.String(required=True, description='status of the item'),
})

bucket = api.model('Bucket', {
    'id': fields.Integer(readOnly=True,
                         description='The unique identifier of a bucketlist'),
    'name': fields.String(required=True, description='Bucketlist name'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.String(required=True, description='Bucketlist owner'),
})
