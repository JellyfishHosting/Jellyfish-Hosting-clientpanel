from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from config import mongo_uri
import flask_pymongo
import string
from zenora import APIClient
import random
import utils.check_maintenance
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
ticket_counter = 1
tickets = []
create_ticket_blueprint = Blueprint('create_ticket', __name__, template_folder='templates')
@create_ticket_blueprint.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
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
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({'email': email})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if request.method == 'POST':
            bearer_client = APIClient(session.get('token'), bearer=True)
            current_user = bearer_client.users.get_current_user()
            email = current_user.email
            title = request.form['title']
            description = request.form['description']
            ticketCollections = mydb['tickets']
            letters = string.ascii_uppercase
            password = ''.join(random.choice(letters) for i in range(10))
            new_ticket = ticketCollections.insert_one({'ticket_id': password, 'title': title, 'description': description, 'email': email})
            ticket = ticketCollections.find_one({'email': email})
            ticket_id=password
            return redirect(url_for('view_ticket.view_ticket', ticket_id=ticket_id))
    else:
        return redirect(url_for('discord.discord'))
    return render_template('create_ticket.html')
