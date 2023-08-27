from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from config import mongo_uri
import utils.check_maintenance
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
list_tickets_blueprint = Blueprint('list_tickets', __name__, template_folder='templates')
@list_tickets_blueprint.route('/list_tickets/', methods=['GET', 'POST'])
def list_tickets():
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
        ticketCollection = mydb['tickets']
        usersCollection = mydb['users']
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        isStaff = usersCollection.find_one({"email": email})
        staff = isStaff.get('staff')
        if staff == "yes":
            ticket = ticketCollection.find({}, {"_id": 0})    
        else:
            ticket = ticketCollection.find({"email": email}, {"_id": 0})
    else:
        return redirect(url_for('discord.discord'))
    return render_template('list_tickets.html', ticket=ticket)
