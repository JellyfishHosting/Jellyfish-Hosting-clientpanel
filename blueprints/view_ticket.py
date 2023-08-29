from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from config import mongo_uri
import flask_pymongo
from zenora import APIClient
from datetime import datetime
import utils.check_maintenance
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
view_ticket_blueprint = Blueprint('view_ticket', __name__, template_folder='templates')
@view_ticket_blueprint.route('/view_ticket/<string:ticket_id>', methods=['GET', 'POST'])
def view_ticket(ticket_id):
    if 'token' in session:
        isMaintenance = utils.check_maintenance.check_maintenance()
        if isMaintenance == "yes":
            bearer_client = APIClient(session.get('token'), bearer=True)
            current_user = bearer_client.users.get_current_user()
            username = current_user.username
            email = current_user.email
            usersCollection = mydb['users']
            data = usersCollection.find_one({'email': email})
            if data.get('staff') == "no":
                return redirect(url_for('maintenance.maintenance'))
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({'email': email})
        reason = isBanned.get('reason')
        if isBanned is not None:
            return render_template('banned.html', reason=reason)
        ticket = None
        ticket_id = None
        ticketCollection = mydb['tickets']
        messageCollection = mydb['messages']
        usersCollection = mydb['users']
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        isStaff = usersCollection.find_one({"email": email})
        if isStaff.get('staff') == "yes":
            ticket_id = ticket_id
            ticket = ticketCollection.find_one({'ticket_id': ticket_id})
        if ticket_id is None:
            ticket_id = ticket.get('ticket_id')
        if ticket is None:
            ticket = ticketCollection.find_one({'email': email})
        messages = messageCollection.find({"ticket_id": ticket_id}, {'_id': 0})
    else:
        return redirect(url_for('discord.discord'))
    return render_template('view_ticket.html', ticket=ticket, ticket_id=ticket_id, messages=messages)
