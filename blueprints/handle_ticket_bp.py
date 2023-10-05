from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from config import mongo_uri
from zenora import APIClient
import flask_pymongo
from datetime import datetime
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

bp = Blueprint('handle_ticket', __name__, template_folder='templates')
"""
Route handler for handling a support ticket.

Parameters:
  - ticket_id: ID of the ticket to handle.

Functionality:
  - Check for valid user session.
  - Get current user info from session.
  - Handle POST request to add message or close ticket.
  - Add new message to database.
  - Close ticket by deleting from DB.
  - Redirect to ticket page or dashboard.
"""
@bp.route('/api/handle_ticket/<string:ticket_id>', methods=['GET', 'POST'])
def handle_ticket(ticket_id):
    if 'token' in session:
        ticketCollection = mydb['tickets']
        messageCollection = mydb['messages']
        usersCollection = mydb['users']
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
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