from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash
from config import oauth_uri, mongo_uri, client_id_paypal, client_secret_paypal
from zenora import APIClient
import flask_pymongo
import paypalrestsdk
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": client_id_paypal,
    "client_secret": client_secret_paypal
})
bp = Blueprint('execute', __name__, template_folder="templates")
@bp.route('/execute', methods=['GET', 'POST'])
def execute():
    item = request.form['item']
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id': request.form['payerID']}):
        print("Execute Success!")
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        data = usersCollection.find_one({'email': email})
        if item == "100% CPU":
            currentCPU = data.get('cpu_limit')
            currentCPU += 100
            filter = {'email': email}
            newValues = { "$set": { 'cpu_limit': currentCPU}}
            usersCollection.update_one(filter, newValues)
        if item == "512MB RAM":
            currentRam = data.get('memory_limit')
            currentRam += 512
            filter = {'email': email}
            newValues = { "$set": {'memory_limit': currentRam}}
            usersCollection.update_one(filter, newValues)
        if item == "1000MB Storage":
            currentStorage = data.get('storage_limit')
            currentStorage += 1000
            filter = {'email': email}
            newValues = { "$set": { 'storage_limit': currentStorage}}
            usersCollection.update_one(filter, newValues)
            return jsonify({'success': success})
        success = True
        flash("Suceess! Your purchase was executed successfully.")
        return redirect(url_for('dashboard.dashboard'))
    else:
        print(payment.error)