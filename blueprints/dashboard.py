from flask import Blueprint, render_template, session, flash, redirect, url_for
from config import client_secret, oauth_uri, redirect_uri, token, mongo_uri
from zenora import APIClient
import flask_pymongo
import utils.check_maintenance
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
dashboard_blueprint = Blueprint('dashboard', __name__, template_folder='templates')
@dashboard_blueprint.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'token' in session:
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
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        usersCollection = mydb['users']
        data = usersCollection.find_one({"email": email})
        storage_limit = data.get('storage_limit')
        memory_limit = data.get('memory_limit')
        cpu_limit = data.get('cpu_limit')
        server_limit = data.get('server_limit')
        serversCollection = mydb['servers']
        serversData = serversCollection.find({'email': email})
        if serversData:
            servers = list(serversData)
            return render_template('dashboard.html', has_server=True, storage_limit=storage_limit, memory_limit=memory_limit, cpu_limit=cpu_limit, server_limit=server_limit, servers=servers)
        else:
            return render_template('dashboard.html', storage_limit=storage_limit, memory_limit=memory_limit, cpu_limit=cpu_limit, server_limit=server_limit, has_server=False)
    else:
        return redirect(url_for('discord.discord'))