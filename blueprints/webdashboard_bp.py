from flask import Blueprint, render_template, session, request, flash, redirect, url_for, jsonify
import requests
from config import token, client_secret, redirect_uri, mongo_uri, directadmin_password, client_id_paypal, client_secret_paypal
from zenora import APIClient
from utils.users import directadmin_create
import flask_pymongo
import random
import string
from datetime import datetime
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

bp = Blueprint('webdashboard', __name__, template_folder="templates")
@bp.route('/webdashboard', methods=['GET', 'POST'])
def webdashboard():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        ip_data = usersCollection.find_one({'email': email})
        ip_addr = ip_data.get('ip_addr')
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({"email": email, 'ip_addr': ip_addr})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        return render_template('web_dashboard.html', client_id_paypal=client_id_paypal)
    else:
        return redirect(url_for('login.login'))

@bp.route('/create_directadmin_account', methods=['GET', 'POST'])
def create_directadmin_account():
    print("asd")
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        username = current_user.username
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        package = request.json['package']
        domain = request.json['domain']
        try:
            directadmin_create(username, email, password, domain, package)
        except Exception as e:
            print(e)
        flash("Success: Your directadmin account has been created! Please check your email.")
        return redirect(url_for('dashboard.dashboard'))
    else:
        return redirect(url_for('login.login'))
