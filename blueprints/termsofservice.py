from flask import Blueprint, render_template, redirect, url_for, session
from config import oauth_uri, mongo_uri
import utils.check_maintenance
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
terms_of_service_blueprint = Blueprint('terms_of_service', __name__, template_folder='templates')
@terms_of_service_blueprint.route('/termsofservice', methods=['GET', 'POST'])
def terms_of_service():
    return render_template('termsofservice.html')