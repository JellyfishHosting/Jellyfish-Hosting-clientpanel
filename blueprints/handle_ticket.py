from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from config import mongo_uri
from zenora import APIClient
import flask_pymongo
from datetime import datetime
import utils.check_maintenance
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

handle_ticket_blueprint = Blueprint('handle_ticket', __name__, template_folder='templates')
@handle_ticket_blueprint.route('/api/handle_ticket/<string:ticket_id>', methods=['GET', 'POST'])
def handle_ticket(ticket_id):
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
        messageCollection = mydb['messages']
        usersCollection = mydb['users']
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        if request.method == 'POST':
            button_pressed = request.form['button_pressed']
            if button_pressed == 'create':
                sender = username
                message = request.form['message']
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_message = {'sender': sender, 'timestamp': timestamp, 'message': message, 'ticket_id': ticket_id}
                messageCollection.insert_one(new_message)
                return redirect(url_for('view_ticket.view_ticket', ticket_id=ticket_id))
            else:
                ticketCollection.delete_one({'ticket_id': ticket_id})
                flash("Success: Successfully deleted the ticket!", 'success')
                return redirect(url_for('dashboard.dashboard'))