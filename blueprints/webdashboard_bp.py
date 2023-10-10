from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from config import token, client_secret, redirect_uri, mongo_uri, directadmin_password
from zenora import APIClient
from utils.users import directadmin_create
import flask_pymongo
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

testbp = Blueprint('webdashboard', __name__, template_folder="templates")
@testbp.route('/webdashboard', methods=['GET', 'POST'])
def webdashboard():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        usersCollection = mydb['users']
        ip_data = usersCollection.find_one({'email': email})
        ip_addr = ip_data.get('ip_addr')
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({"email": email, 'ip_addr': ip_addr})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if request.method == "POST":
            domain = request.form.get('domain')
            password = request.form.get('password')
            email = request.form.get('email')
            username = request.form.get('username')
            package = request.form.get('package')
            if package == "tier1":
                package="tier1package"
            if package == "tier2":
                package="tier2package"
            if package == "tier3":
                package="tier3package"
            try:
                directadmin_create(username=username, email=email, password=password, domain=domain, package=package)
            except Exception as e:
                print(e)
            flash("Success: Successfully created web account. Email supplied has been notified.")
            return redirect(url_for('webdashboard.webdashboard'))
    else:
        return redirect(url_for('login.login'))
    return render_template("web_dashboard.html")