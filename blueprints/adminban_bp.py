from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from config import oauth_uri, mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('admin_ban', __name__, template_folder='templates')
@bp.route('/admin/ban', methods=['GET', 'POST'])
def admin_ban():
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        banCollection = mydb['bans']
        usersCollection = mydb['users']
        isStaff = usersCollection.find_one({'email': email})
        if isStaff.get('staff') == "no":
            flash("Error: You don't have the right permission to access this page.", "error")
            return redirect(url_for('dashboard.dashboard'))
        if request.method == "POST":
            username = request.form.get('username')
            reason = request.form.get('reason')
            data = usersCollection.find_one({'username': username})
            if data == None:
                flash("Error: There is no one under this username.", 'error')
                return redirect(url_for('admin_ban.admin_ban'))
            email = data.get('email')
            banCollection.insert_one({'email': email, 'username': username, 'reason': reason})
            flash("Success: User has successfully been banned")
            return redirect(url_for('admin_ban.admin_ban'))
    else:
        return redirect(url_for('login.login'))
    return render_template("ban.html")