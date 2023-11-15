from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from config import mongo_uri
from zenora import APIClient
import datetime
import flask_pymongo
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('renewal', __name__, template_folder="templates")
@bp.route('/api/renewal', methods=['GET', 'POST'])
def renewal():
    if "token" in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        serversCollection = mydb['servers']
        server_name = request.form['server_name']
        server_data = serversCollection.find_one({'server_name': server_name})
        renewal_date_string = server_data.get('renewal_date')
        date_format = '%Y-%m-%d'
        old_renewal_date = datetime.datetime.strptime(renewal_date_string, date_format)
        formatted_renewal_date = old_renewal_date + datetime.timedelta(days=7)
        new_renewal_date = formatted_renewal_date.strftime(date_format)
        serversCollection.update_one({'server_name': server_name}, {'$set': {'renewal_date': new_renewal_date}})
        flash('Success: Successfully renewed your server!', 'success')
        return redirect(url_for('dashboard.dashboard'))