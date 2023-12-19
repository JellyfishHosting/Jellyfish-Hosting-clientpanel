from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from config import mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('admin_announce', __name__, template_folder='templates')
@bp.route('/admin/announce', methods=['GET', 'POST'])
def admin_announce():
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        isStaff = usersCollection.find_one({'email': email})
        if isStaff.get('staff') == "no":
            flash("Error: You don't have the right permission to access this page.", "error")
            return redirect(url_for('dashboard.dashboard'))
    else:
        return redirect(url_for('login.login'))
    return render_template("announce.html")