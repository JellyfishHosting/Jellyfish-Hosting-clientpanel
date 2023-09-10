from flask import Blueprint, render_template, redirect, url_for, session
bp = Blueprint('dashboard', __name__, template_folder='templates')
@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')