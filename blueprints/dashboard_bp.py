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

bp = Blueprint('dashboard', __name__, template_folder='templates')
@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'token' in session:
        announcementCollection = mydb['announcements']
        announcements = announcementCollection.find()
        announcements = list(announcements)
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        usersCollection = mydb['users']
        ip_data = usersCollection.find_one({'email': email})
        ip_addr = ip_data.get('ip_addr')
        banCollection = mydb['bans']
        data = usersCollection.find_one({"email": email})
        storage_limit = data.get('storage_limit')
        memory_limit = data.get('memory_limit')
        cpu_limit = data.get('cpu_limit')
        server_limit = data.get('server_limit')
        serversCollection = mydb['servers']
        serversData = serversCollection.find({'email': email})
        isBanned = banCollection.find_one({'email': email, 'ip_addr': ip_addr})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if serversData:
            servers = list(serversData)
            if announcements == None:
              return render_template('dashboard.html', has_server=True, storage_limit=storage_limit, memory_limit=memory_limit, cpu_limit=cpu_limit, server_limit=server_limit, servers=servers)
            else:
              return render_template('dashboard.html', has_server=True, storage_limit=storage_limit, memory_limit=memory_limit, cpu_limit=cpu_limit, server_limit=server_limit, servers=servers, announcements=announcements)
        else:
            if announcements == None:  
              return render_template('dashboard.html', storage_limit=storage_limit, memory_limit=memory_limit, cpu_limit=cpu_limit, server_limit=server_limit, has_server=False)
            else:
               return render_template('dashboard.html', storage_limit=storage_limit, memory_limit=memory_limit, cpu_limit=cpu_limit, server_limit=server_limit, has_server=False, announcements=announcements)
    else:
        return redirect(url_for('login.login'))