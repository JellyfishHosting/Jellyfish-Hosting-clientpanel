from flask import Blueprint, render_template, request, session, redirect, url_for
from config import mongo_uri
import flask_pymongo
from zenora import APIClient
from datetime import datetime
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('view_ticket', __name__, template_folder='templates')
@bp.route('/view_ticket/<string:ticket_id>', methods=['GET', 'POST'])
def view_ticket(ticket_id):
    if 'token' in session:
        announcementCollection = mydb['announcements']
        announcements = announcementCollection.find()
        announcements = list(announcements)
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        ticket = None
        ticket_id = None
        ticketCollection = mydb['tickets']
        messageCollection = mydb['messages']
        usersCollection = mydb['users']
        ip_data = usersCollection.find_one({'email': email})
        ip_addr = ip_data.get('ip_addr')
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({"email": email, 'ip_addr': ip_addr})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        isStaff = usersCollection.find_one({"email": email})
        if isStaff.get('staff') == "yes":
            ticket_id = ticket_id
            ticket = ticketCollection.find_one({'ticket_id': ticket_id})
        if ticket is None:
            ticket = ticketCollection.find_one({'email': email})
        if ticket_id is None:
            ticket_id = ticket.get('ticket_id')
        messages = messageCollection.find({"ticket_id": ticket_id}, {'_id': 0})
    else:
        return redirect(url_for('login.login'))
    if announcements == None:
        return render_template('view_ticket.html', ticket=ticket, ticket_id=ticket_id, messages=messages)
    else:
        return render_template('view_ticket.html', ticket=ticket, ticket_id=ticket_id, messages=messages, announcements=announcements)