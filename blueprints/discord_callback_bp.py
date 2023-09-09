from flask import Blueprint, render_template, redirect, url_for, session, request
from config import oauth_uri, mysql_uri, token, client_secret, redirect_uri, mysql_user, mysql_password, mysql_database
from zenora import APIClient
import mysql.connector
import random
import string

mydb = mysql.connector.connect(
    host=mysql_uri,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)

client = APIClient(token, client_secret=client_secret)
bp = Blueprint('discord_callback', __name__, template_folder='templates')
@bp.route('/oauth/discord/callback', methods=['GET', 'POST'])
def discord_callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, redirect_uri).access_token
    session['token'] = access_token
    mycursor = mydb.cursor()
    mycursor.execute("CREATE TABLE users (email VARCHAR(255), username VARCHAR(255), password VARCHAR(255), memory INTEGER, cpu INTEGER, ram INTEGER)")
    bearer_client = APIClient(session.get('token'), bearer=True)
    current_user = bearer_client.users.get_current_user()
    username = current_user.username
    email = current_user.email
    letters = string.ascii_uppercase
    password = ''.join(random.choice(letters) for i in range(10))
    sql = "INSERT INTO users (email, username, password, memory, cpu, ram) VALUES (%s, %s, %s, %s, %s)"
    val = (username, email, password, 10000, 100, 2000)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect('/login')