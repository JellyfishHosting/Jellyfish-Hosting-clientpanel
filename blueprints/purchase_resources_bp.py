from flask import Blueprint, render_template, redirect, url_for, session
from config import oauth_uri
from zenora import APIClient
bp = Blueprint('purchase_resources', __name__, template_folder="templates")
@bp.route('/purchase_resources', methods=['GET', 'POST'])
def purchase_resources():
    if "token" in session:
        return render_template('purchase_resource.html')
    else:
        return redirect(url_for('login.login'))