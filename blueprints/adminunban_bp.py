from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from config import oauth_uri, mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint("admin_unban", __name__, template_folder='templates')
"""
Route handler for admin user unban page.

Checks for valid admin session and permissions.
Gets admin user info from API using session token.
Handles form POST request to unban user.
Looks up user in MongoDB by username from form.
Gets user email from MongoDB document.
Checks if user is banned in bans collection.
Deletes ban document to unban user if found.
Sends success/error flash messages.
Redirects back to admin unban page.

Renders unban page template on GET request. 
Redirects to login if no valid session.
"""
@bp.route('/admin/unban', methods=['GET', 'POST'])
def admin_unban():
    if "token" in session:
        announcementCollection = mydb['announcements']
        announcements = announcementCollection.find()
        announcements = list(announcements)
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        banCollection = mydb['bans']
        usersCollection = mydb['users']
        isStaff = usersCollection.find_one({'email': email})
        if isStaff.get('staff') == "no":
            flash("Error: You don't have the right permission to access this page.")
            return redirect(url_for('dashboard.dashboard'))
        if request.method == "POST":
            username = request.form.get('username')
            reason = request.form.get('reason')
            data = usersCollection.find_one({'username': username})
            if data == None:
                flash("Error: There is no one under this username.", 'error')
                return redirect(url_for('admin_unban.admin_unban'))
            email = data.get('email')
            isBanned = banCollection.find_one({'email': email})
            if isBanned is not None:
                banCollection.delete_one({'email': email})
                flash("Success: User has successfully been unbanned.", 'success')
                return redirect(url_for('admin_unban.admin_unban'))
            else:
                flash("Error: The username you have entered is not banned.", 'error')
                return redirect(url_for('admin_unban.admin_unban'))
    else:
        return redirect(url_for('login.login'))
    if announcements == None:
        return render_template('unban.html')
    else:
        return render_template('unban.html', announcements=announcements)

