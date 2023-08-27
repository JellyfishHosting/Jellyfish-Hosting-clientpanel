from flask import Blueprint, render_template, redirect, url_for, session
import utils.check_maintenance
from config import mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
index_blueprint = Blueprint('index', __name__, template_folder='templates')
@index_blueprint.route('/')
def index():
    isMaintenance = utils.check_maintenance.check_maintenance()
    if isMaintenance == "yes":
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        usersCollection = mydb['users']
        data = usersCollection.find_one({'email': email})
        if data.get('staff') == "no":
            return redirect(url_for('maintenance.maintenance'))
    return render_template('index.html')