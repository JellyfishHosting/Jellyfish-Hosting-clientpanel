from flask import Blueprint, render_template, redirect, url_for, session, flash
from config import oauth_uri, mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('admin_dashboard', __name__, template_folder='templates')
@bp.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        usersCollection = mydb['users']
        isStaff = usersCollection.find_one({'email': email})
        if isStaff.get('staff') == "no":
            flash("Error: You don't have the right permissions to access this page.", "error")
            return redirect(url_for('dashboard.dashboard'))
        serversCollection = mydb['servers']
        userData = usersCollection.count_documents({})
        serverData = serversCollection.count_documents({})
        staffData = usersCollection.count_documents({"staff": "yes"})
        banData = 0
        totalUsers = userData
        totalServers = serverData
        totalBans = banData
        totalStaff = staffData
    return render_template('admin.html', totalUsers=totalUsers, totalServers=totalServers, totalBans=totalBans, totalStaff=totalStaff)