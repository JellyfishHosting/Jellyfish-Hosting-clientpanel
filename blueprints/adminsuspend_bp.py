from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from config import mongo_uri, sendgrid_api_key
import flask_pymongo
from zenora import APIClient
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import utils.server
sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('admin_suspend', __name__, template_folder='templates')
"""
Route handler for admin server suspension page.

Checks for valid admin user session and permissions.
Gets current admin user info from API using session token.  
Handles form POST request to suspend server.
Gets server name from form and finds server in MongoDB.
Gets server email and ID from MongoDB document.
Calls utility function to suspend server by ID.
Sends email notification to server owner.
Redirects back to admin suspension page.

Renders suspension page template on GET request.
Redirects to login if no valid session.
"""
@bp.route('/admin/suspend', methods=['GET', 'POST'])
def admin_suspend():
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        serversCollection = mydb['servers']
        isStaff = usersCollection.find_one({'email': email})
        if isStaff.get('staff') == "no":
            flash("Error: You don't have the right permission to access this page.", 'error')
            return redirect(url_for('dashboard.dashboard'))
        if request.method == 'POST':
            server_name = request.form.get('server_name')
            reason = request.form.get('reason')
            data = serversCollection.find_one({'server_name': server_name})
            if data == None:
                flash("Error: There is no server under this name.", 'error')
                return redirect(url_for('admin_suspend.admin_suspend'))
            server_email = data.get('email')
            server_id = data.get('server_id')
            utils.server.suspend_server(server_id=server_id)
            flash("Success: The server has successfully been suspended.")
            from_email = Email('no-reply@jellyfishhosting.xyz')
            to_email = To(server_email)
            subject = "Jellyfish Hosting - Your server has been suspended!"
            content = Content('text/html', f'<p>Your server has been suspended for the reason: {reason}</p><p>Please contact our administrators by clicking <a href="https://my.jellyfishhosting.xyz/create_ticket">here</a> if you think this is a mistake.</p><p>Kind Regards,</p><p>Jellyfish Hosting</p>')
            mail = Mail(from_email, to_email, subject, content)
            mail_json = mail.get()
            response = sg.client.mail.send.post(request_body=mail_json)
            return redirect(url_for('admin_suspend.admin_suspend'))
    else:
        return redirect(url_for('login.login'))
    return render_template('suspend.html')