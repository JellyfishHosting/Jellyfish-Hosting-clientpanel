from flask import Blueprint, render_template, session, request, flash, redirect, url_for, jsonify
import requests
from config import token, client_secret, redirect_uri, mongo_uri, directadmin_password, client_id_paypal, client_secret_paypal
from zenora import APIClient
from utils.users import alert_vpn
import flask_pymongo
import random
import string
from datetime import datetime
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

bp = Blueprint('vpnservice', __name__, template_folder="templates")
@bp.route('/vpnservice', methods=['GET', 'POST'])
def vpnservice():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({"email": email})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        return render_template('vpnservice.html', client_id_paypal=client_id_paypal)
    else:
        return redirect(url_for('login.login'))

@bp.route('/alert_vpn_admins', methods=['GET', 'POST'])
def alert_vpn_admins():
    print("asd")
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        package = request.json['location']
        name = request.json['name']
        try:
            alert_vpn(name, email, package)
        except Exception as e:
            print(e)
        flash("Success: We have alerted the VPN Administrators to create your account. If they do not contact you by email within the next 24 hours please create a ticket.")
        return redirect(url_for('dashboard.dashboard'))
    else:
        return redirect(url_for('login.login'))
