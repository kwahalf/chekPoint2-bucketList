# app/__init__.py

from .restplus import api
from flask import Flask, Blueprint
from flask_restplus import Api


# local import
from instance.config import app_config
from .bucketlist_api.endpoints.auth.views import ns  as auth_namespace
from .bucketlist_api.endpoints.bucketlists.views import ns as bucketlists_namespace 
from .bucketlist_api.models import db

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    api.add_namespace(auth_namespace)
    api.add_namespace(bucketlists_namespace)
    api.init_app(app)

    return app
