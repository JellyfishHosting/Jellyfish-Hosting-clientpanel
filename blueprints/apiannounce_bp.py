from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from config import mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('api_announce', __name__, template_folder='templates')
@bp.route('/api/announce', methods=['GET', 'POST'])
def api_announce():
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        announcementCollection = mydb['announcements']
        isStaff = usersCollection.find_one({'email': email})
        if isStaff.get('staff') == "no":
            flash("Error: You don't have the right permission to use this API request.", "error")
            return redirect(url_for('dashboard.dashboard'))
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']

            announcement = {'title': title, 'description': description}
            announcementCollection.insert_one(announcement)
            flash("Success: Announcement has been sent site wide.", 'success')
    else:
        return redirect(url_for('login.login'))
    return redirect(url_for('admin_announce.admin_announce'))