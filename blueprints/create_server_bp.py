from flask import Blueprint, render_template, session, request, url_for, redirect, flash
from config import oauth_uri
import utils.server
from utils.nodes import get_node_details
from zenora import APIClient
import flask_pymongo
from config import mongo_uri
import json
import utils.users
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

LOCATION_IDS = {"uk": 1, "de": 2}
NODE_IDS = {"UK1": 1, "DE1": 2}

"""
Route handler for creating a new server. 

Parameters:
- None directly, but uses session data and form data from requests.

Functionality:
- Checks for valid user session.
- Gets user info from session.
- Validates form data for creating server.
- Checks user resource limits for server creation.
- Maps user inputs to IDs for location, node, etc.
- Inserts new server data into DB.
- Updates user resource limits in DB.
- Calls utility to create server on backend.
- Handles success and error cases.
- Renders create server page or redirects on completion.
"""

bp = Blueprint('create_server', __name__, template_folder='templates')
@bp.route('/create_server', methods=['GET', 'POST'])
def create_server():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        email = current_user.email
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({'email': email})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if request.method == 'POST':
            server_name = request.form.get('serverName')
            description = request.form.get('description')
            cpu_limit = int(request.form.get('cpuLimit'))
            ram = int(request.form.get('ram'))
            storage = int(request.form.get('storage'))
            location = request.form.get('location')
            node = request.form.get('node')
            category = request.form.get('category')
            software = request.form.get('software')
            if location in LOCATION_IDS:
                locationid = LOCATION_IDS[location]
            if node in NODE_IDS:
                nodeid = NODE_IDS[node]
            if category == "minecraft":
                nestid = 1
                if software in ["Forge Minecraft", "Bungeecord", "Vanilla Minecraft", 
                "Paper", "Sponge (SpongeVanilla)"]:
                    eggid = [1, 2, 3, 4, 5][["Forge Minecraft", "Bungeecord", 
                            "Vanilla Minecraft", "Paper", 
                            "Sponge (SpongeVanilla)"].index(software)]
            if category == "voice":
                nestid = 3
                if software in ["Mumble Server", "Teamspeak3 Server"]:
                    eggid = [12, 13][["Mumble Server", "Teamspeak3 Server"].index(software)]
            if category == "discord":
                nestid = 5
                if software in ["Discord JS", "Discord JS (typescript)"]:  
                    eggid = [15, 16][["Discord JS", "Discord JS (typescript)"].index(software)]
            result = utils.users.list_users_with_email(email=email)
            user_id = result[0]['attributes']['id']
            usersCollections = mydb['users']
            data = usersCollections.find_one({'email': email})
            current_cpu_limit = data.get('cpu_limit')
            current_ram_limit = data.get('memory_limit')
            current_server_limit = data.get('server_limit')
            actual_current_server_limit = current_server_limit - 1
            current_storage_limit = data.get('storage_limit')
            if current_cpu_limit < cpu_limit:
                flash("Error: You don't have enough cpu", 'error')
                return render_template('create_server.html')
            if int(current_ram_limit) < int(ram):
                flash("Error: You don't have enough ram", 'error')
                return render_template('create_server.html')
            if int(actual_current_server_limit) <= 0:
                flash("Error: You ran out of server creations", 'error')
                return render_template('create_server.html')
            if int(current_storage_limit) < int(storage):
                flash("Error: You don't have enough storage", 'error')
                return render_template('create_server.html')
            cpu_limit_db = current_cpu_limit - cpu_limit
            ram_limit_db = int(current_ram_limit) - int(ram)
            server_limit_db = int(actual_current_server_limit)
            storage_limit_db = int(current_storage_limit) - int(storage)
            location_ids = [locationid]
            serversCollection = mydb['servers']
            filter = {'email': email}
            newValues = { "$set": { 'cpu_limit': cpu_limit_db, 'memory_limit': ram_limit_db, 'server_limit': server_limit_db, 'storage_limit': storage_limit_db}}
            usersCollections.update_one(filter, newValues)
            try:
                result = utils.server.create_server(name=server_name, user_id=user_id, nestid=nestid, eggid=eggid, ram=ram, storage=storage, location_ids=location_ids, cpu_limit=cpu_limit, description=description)
                resultContent = result.content
                requests = json.loads(resultContent)
                server_id = requests['attributes']['id']
                serversCollection.insert_one({"server_name": server_name, "cpu": cpu_limit, "ram": ram, "storage": storage, "email": email, 'server_id': server_id})
                flash('Success: Server created successfully!', 'success')
                return redirect(url_for('dashboard.dashboard'))
            except Exception as e:
                print(e)
                flash('Error: There was an issue when creating the server! Please contact the main developers.', 'error')
                return render_template('create_server.html')
    else:
        return redirect(url_for('login.login'))
    return render_template('create_server.html')