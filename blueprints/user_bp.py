from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from config import token, client_secret, redirect_uri, mongo_uri
from zenora import APIClient
import flask_pymongo
from utils.users import update_user
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

bp = Blueprint('user', __name__, template_folder='templates')
@bp.route('/user', methods=['GET', 'POST'])
def user():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        username = current_user.username
        email = current_user.email
        user_id = current_user.id
        avatar = current_user.avatar_url
        usersCollection = mydb['users']
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({"email": email})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if request.method == 'POST':
            password = request.form.get('password')
            update_user(email, password)
            filter = {'email': email}
            newValues = { '$set': {"password": password}}
            try:
                usersCollection.update_one(filter, newValues)
                flash("Success: you have changed your game panel password!", 'success')
                return redirect(url_for('dashboard.dashboard'))
            except:
                flash("Error: There was an error changing your game panel password. Please contact the main developers.", 'error')
                return redirect(url_for('user.user'))
        else:
            result = usersCollection.find_one({'email': email})
            password = result.get('password')
    else:
        return redirect(url_for('login.login'))
    return render_template('user.html', password=password, user_id=user_id, username=username, avatar=avatar)