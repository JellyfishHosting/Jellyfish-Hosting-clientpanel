from flask import Blueprint, render_template, redirect, url_for, session
from config import oauth_uri, mongo_uri
import utils.check_maintenance
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
privacy_policy_blueprint = Blueprint('privacy_policy', __name__, template_folder='templates')
@privacy_policy_blueprint.route('/privacypolicy', methods=['GET', 'POST'])
def privacy_policy():
    return render_template('privacypolicy.html')