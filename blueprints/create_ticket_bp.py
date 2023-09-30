from flask import Blueprint, render_template, request, session, redirect, url_for
from config import mongo_uri
import flask_pymongo
import string
from zenora import APIClient
import random
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
ticket_counter = 1
tickets = []
bp = Blueprint('create_ticket', __name__, template_folder='templates')
@bp.route('/create_ticket', methods=['GET', 'POST'])
def create_ticket():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        banCollection = mydb['bans']
        usersCollection = mydb['users']
        ip_data = usersCollection.find_one({'email': email})
        ip_addr = ip_data.get('ip_addr')
        isBanned = banCollection.find_one({'email': email, 'ip_addr': ip_addr})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            ticketCollections = mydb['tickets']
            letters = string.ascii_uppercase
            ticket_id = ''.join(random.choice(letters) for i in range(10))
            new_ticket = ticketCollections.insert_one({'ticket_id': ticket_id, 'title': title, 'description': description, "email": email})
            return redirect(url_for('view_ticket.view_ticket', ticket_id=ticket_id))
    else:
        return redirect(url_for('login.login'))
    return render_template('create_ticket.html')