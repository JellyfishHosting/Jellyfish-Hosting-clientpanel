from flask import Blueprint, render_template, redirect, url_for, session
from config import mongo_uri
import flask_pymongo
from zenora import APIClient
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

"""Route handler for the user dashboard page.

Parameters:
  - session: User session data containing the auth token.

Functionality:
  - Check for valid user session.
  - Get user info from API using session token.
  - Lookup user resource limits in MongoDB.
  - Get user's servers from MongoDB.
  - Pass data to template to render dashboard page.
  - If no valid session, redirect to login.
"""

bp = Blueprint('joinforresources', __name__, template_folder='templates')
@bp.route('/joinforresources', methods=['GET', 'POST'])
def joinforresources():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        ip_data = usersCollection.find_one({'email': email})
        ip_addr = ip_data.get('ip_addr')
        banCollection = mydb['bans']
        jfrCollection = mydb['jfrservers']
        jfrData = jfrCollection.find({}, {"_id": 0})
        isBanned = banCollection.find_one({'email': email, 'ip_addr': ip_addr})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if jfrData:
            jfr = list(jfrData)
            return render_template('joinforresources.html', jfr=jfr)
        else:
            return render_template('joinforresources.html')
    else:
        return redirect(url_for('login.login'))