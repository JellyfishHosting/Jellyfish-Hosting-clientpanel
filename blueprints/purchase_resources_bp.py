from flask import Blueprint, render_template, redirect, url_for, session
from config import oauth_uri, mongo_uri
from zenora import APIClient
import flask_pymongo
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']
bp = Blueprint('purchase_resources', __name__, template_folder="templates")
@bp.route('/purchase_resources', methods=['GET', 'POST'])
def purchase_resources():
    if "token" in session:
        announcementCollection = mydb['announcements']
        announcements = announcementCollection.find()
        announcements = list(announcements)
        if announcements == None:
            return render_template('purchase_resource.html')
        else:
            return render_template('purchase_resource.html', announcements=announcements)
    else:
        return redirect(url_for('login.login'))