from flask import Blueprint, render_template, request, session, redirect, url_for
from config import mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('list_tickets', __name__, template_folder='templates')
# Blueprint to handle listing tickets
# Checks for valid user session 
# Gets current user info from API
# Checks if user is banned
# If staff, gets all tickets
# Else gets tickets for current user
# Renders template to display tickets
@bp.route('/list_tickets', methods=['GET', 'POST'])
def list_tickets():
    if 'token' in session:
        announcementCollection = mydb['announcements']
        announcements = announcementCollection.find()
        announcements = list(announcements)
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        ticketCollection = mydb['tickets']
        banCollection = mydb['bans']
        ip_data = usersCollection.find_one({'email': email})
        ip_addr = ip_data.get('ip_addr')
        isBanned = banCollection.find_one({"email": email, 'ip_addr': ip_addr})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        isStaff = usersCollection.find_one({"email": email})
        if isStaff.get('staff') == "yes":
            ticket = ticketCollection.find({}, {"_id": 0})
        else:
            ticket = ticketCollection.find({"email": email}, {"_id": 0})
    else:
        return redirect(url_for('login.login'))
    if announcements == None:
        return render_template('list_tickets.html', ticket=ticket)
    else:
        return render_template('list_tickets.html', ticket=ticket, announcements=announcements)