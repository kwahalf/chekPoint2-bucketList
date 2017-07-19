# app/__init__.py
#from flask_restplus import Api
from .restplus import api
from flask import Flask, Blueprint
from flask_restplus import Api
#from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config
from .bucketlist_api.endpoints.auth.views import ns  as auth_namespace
from .bucketlist_api.endpoints.bucketlists.views import ns as bucketlists_namespace 
from .bucketlist_api.models import db
# initialize sql-alchemy
#db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    #blueprint = Blueprint('api', __name__, url_prefix='/api', )
    api.add_namespace(auth_namespace)
    api.add_namespace(bucketlists_namespace)
    api.init_app(app)
    #app.register_blueprint(blueprint)

    return app
