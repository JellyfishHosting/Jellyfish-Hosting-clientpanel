from flask import Blueprint, render_template, redirect, url_for
from config import oauth_uri
import utils.check_maintenance
maintenance_blueprint = Blueprint('maintenance', __name__, template_folder='templates')
@maintenance_blueprint.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    return render_template('maintenance.html', oauth_uri=oauth_uri)