from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from config import oauth_uri, mongo_uri, sendgrid_api_key
import flask_pymongo
from zenora import APIClient
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('admin_ban', __name__, template_folder='templates')
"""
Route handler for admin user account banning page. 

Checks for admin user session and validates permissions.
Gets current admin user info from API using session token.
Handles form POST request to ban user account.
Gets username from form and finds user in MongoDB.
Gets user email and IP address from MongoDB document.
Inserts ban document into MongoDB bans collection.
Sends email notification to banned user.
Redirects back to admin ban page.

Renders ban page template on GET request.
Redirects to login if no valid session.
"""
@bp.route('/admin/ban', methods=['GET', 'POST'])
def admin_ban():
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
            flash("Error: You don't have the right permission to access this page.", "error")
            return redirect(url_for('dashboard.dashboard'))
        if request.method == "POST":
            username = request.form.get('username')
            reason = request.form.get('reason')
            data = usersCollection.find_one({'username': username})
            if data == None:
                flash("Error: There is no one under this username.", 'error')
                return redirect(url_for('admin_ban.admin_ban'))
            user_email = data.get('email')
            ip_addr = data.get('ip_addr')
            banCollection.insert_one({'email': user_email, 'username': username, 'reason': reason, 'ip_addr': ip_addr})
            flash("Success: User has successfully been banned")
            from_email = Email('no-reply@jellyfishhosting.xyz')
            to_email = To(user_email)
            subject = "Jellyfish Hosting - Your account has been banned!"
            content = Content('text/html', f'<p>Your account has been banned for the reason: {reason}.</p><p>Please contact our administrators by emailing us at jellyfishhosting@gmail.com if you think this is a mistake.</p><p>Kind Regards,</p><p>Jellyfish Hosting</p>')
            mail = Mail(from_email, to_email, subject, content)
            mail_json = mail.get()
            response = sg.client.mail.send.post(request_body=mail_json)
            return redirect(url_for('admin_ban.admin_ban'))
    else:
        return redirect(url_for('login.login'))
    if announcements == None:
        return render_template("ban.html")
    else:
        return render_template("ban.html", announcements=announcements)