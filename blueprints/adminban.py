from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from config import oauth_uri, mongo_uri
import utils.check_maintenance
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
admin_ban_blueprint = Blueprint('admin_ban', __name__, template_folder='templates')
@admin_ban_blueprint.route('/admin/ban', methods=['GET', 'POST'])
def admin_ban():
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
        if request.method == "POST":
            username = request.form.get('username')
            reason = request.form.get('reason')
            banCollection = mydb['bans']
            userCollection = mydb['users']
            data = userCollection.find_one({'username': username})
            if data == None:
                flash("Error: There is no one under this username.", 'error')
            email = data.get('email')
            banCollection.insert_one({'email': email, 'username': username, 'reason': reason})
            flash("Success: User has successfully been banned.")

    return render_template('ban.html')