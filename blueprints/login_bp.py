from flask import Blueprint, render_template, redirect, url_for, session
from config import oauth_uri, mysql_uri
from zenora import APIClient
bp = Blueprint('login', __name__, template_folder='templates')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', oauth_uri=oauth_uri)