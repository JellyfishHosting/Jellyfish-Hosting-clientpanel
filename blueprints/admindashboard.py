from flask import Blueprint, render_template, redirect, url_for, session, flash
from config import oauth_uri, mongo_uri
import utils.check_maintenance
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
admin_dashboard_blueprint = Blueprint('admin_dashboard', __name__, template_folder='templates')
@admin_dashboard_blueprint.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
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
    bearer_client = APIClient(session.get('token'), bearer=True)
    current_user = bearer_client.users.get_current_user()
    username = current_user.username
    email = current_user.email
    banCollection = mydb['bans']
    isBanned = banCollection.find_one({'email': email})
    if isBanned is not None:
        reason = isBanned.get('reason')
        return render_template('banned.html', reason=reason)
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        usersCollection = mydb['users']
        isStaff = usersCollection.find_one({'email': email})
        if isStaff.get('staff') == "no":
            flash("Error: You don't have the right permission to access this page.")
            return redirect(url_for('dashboard.dashboard'))
        serversCollection = mydb['servers']
        banCollection = mydb['bans']
        userData = usersCollection.count_documents({})
        serverData = serversCollection.count_documents({})
        staffData = usersCollection.count_documents({"staff": "yes"})
        banData = banCollection.count_documents({})
        totalUsers = userData
        totalServers = serverData
        totalBans = banData
        totalStaff = staffData
    return render_template('admin.html', totalUsers=totalUsers, totalServers=totalServers, totalBans=totalBans, totalStaff=totalStaff)