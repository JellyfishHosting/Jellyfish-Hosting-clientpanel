from flask import Blueprint, render_template, request, session, redirect
from config import token, client_secret, redirect_uri, mongo_uri
from zenora import APIClient
import flask_pymongo
import string
import random
import utils.users


mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

client = APIClient(token, client_secret=client_secret)
discord_callback_blueprint = Blueprint('discord_callback', __name__, template_folder='templates')
@discord_callback_blueprint.route('/oauth/discord/callback', methods=['GET', 'POST'])
def discord_callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, redirect_uri).access_token
    session['token'] = access_token
    usersCollection = mydb['users']
    bearer_client = APIClient(session.get('token'), bearer=True)
    current_user = bearer_client.users.get_current_user()
    username = current_user.username
    email = current_user.email
    data = usersCollection.find_one({"email": email})
    if data:    
        return redirect('/dashboard')
    else:
        letters = string.ascii_uppercase
        password = ''.join(random.choice(letters) for i in range(10))
        result = utils.users.create_user(username, email, password)
        usersCollection.insert_one({'email': email, 'username': username, 'password': password, "storage_limit": "10000", "memory_limit": "2000", "cpu_limit": 100, "server_limit": 2})
        return redirect('/dashboard')