from flask import Blueprint, render_template, redirect, url_for, session
from config import oauth_uri, mongo_uri
import utils.check_maintenance
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
discord_blueprint = Blueprint('discord', __name__, template_folder='templates')
@discord_blueprint.route('/discord', methods=['GET', 'POST'])
def discord():
    isMaintenance = utils.check_maintenance.check_maintenance()
    if isMaintenance == "yes":
        if "token" in session:
            bearer_client = APIClient(session.get('token'), bearer=True)
            current_user = bearer_client.users.get_current_user()
            username = current_user.username
            email = current_user.email
            usersCollection = mydb['users']
            data = usersCollection.find_one({'email': email})
            if data.get('staff') == "no":
                return redirect(url_for('maintenance.maintenance'))
    return render_template('discord.html', oauth_uri=oauth_uri)