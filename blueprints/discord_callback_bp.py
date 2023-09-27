from flask import Blueprint, render_template, redirect, url_for, session, request
from config import oauth_uri, token, client_secret, redirect_uri, mongo_uri
from zenora import APIClient
import flask_pymongo
import random
import string
from utils.users import create_user

mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

"""
Route handler for the Discord OAuth callback.

Parameters:
  - code: Authorization code from Discord OAuth flow.
  - session: Flask session to store access token.

Functionality:
  - Exchange code for Discord access token. 
  - Store access token in session.
  - Check if user exists in DB.
  - If not, create new user with random password.
  - Insert user into DB with default resource limits.
  - Redirect to dashboard after login flow.
"""


client = APIClient(token, client_secret=client_secret)
bp = Blueprint('discord_callback', __name__, template_folder='templates')
@bp.route('/oauth/discord/callback', methods=['GET', 'POST'])
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
        result = create_user(username, email, password)
        usersCollection.insert_one({'email': email, 'username': username, 'password': password, "storage_limit": 10000, "memory_limit": 2000, "cpu_limit": 100, "server_limit": 2})
        return redirect('/dashboard')