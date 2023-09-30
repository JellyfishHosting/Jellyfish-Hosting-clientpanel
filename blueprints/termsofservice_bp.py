from flask import Blueprint, render_template, redirect, url_for, session
from config import oauth_uri
from zenora import APIClient
bp = Blueprint('termsofservice', __name__, template_folder="templates")
@bp.route('/termsofservice', methods=['GET', 'POST'])
def login():
    return render_template('termsofservice.html')