from flask import Blueprint, render_template, session, request, url_for, redirect, flash
from config import oauth_uri
import utils.server
import utils.nodes
from zenora import APIClient
import flask_pymongo
from config import mongo_uri
import utils.users
import utils.check_maintenance
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

create_server_blueprint = Blueprint('create_server', __name__, template_folder='templates')
@create_server_blueprint.route('/create_server', methods=['GET', 'POST'])
def create_server():
    if 'token' in session:
        isMaintenance = utils.check_maintenance.check_maintenance()
        if isMaintenance == "yes":
            bearer_client = APIClient(session.get('token'), bearer=True)
            current_user = bearer_client.users.get_current_user()
            username = current_user.username
            email = current_user.email
            usersCollection = mydb['users']
            data = usersCollection.find_one({'email': email})
            if data.get('staff') == "no":
                return redirect(url_for('maintenance.maintenance'))
        banCollection = mydb['bans']
        isBanned = banCollection.find_one({'email': email})
        if isBanned is not None:
            reason = isBanned.get('reason')
            return render_template('banned.html', reason=reason)
        if request.method == 'POST':
            bearer_client = APIClient(session.get('token'), bearer=True)
            current_user = bearer_client.users.get_current_user()
            email = current_user.email
            server_name = request.form.get('serverName')
            description = request.form.get('description')
            cpu_limit = int(request.form.get('cpuLimit'))
            ram = int(request.form.get('ram'))
            storage = int(request.form.get('storage'))
            location = request.form.get('location')
            node = request.form.get('node')
            category = request.form.get('category')
            software = request.form.get('software')
            if location == "uk":
                locationid = 1
            if location == "de":
                locationid = 2
            if node == "UK1":
                nodeid = 1
            if node == "DE1":
                nodeid = 2
            if category == "minecraft":
                nestid = 1
                if software == "Forge Minecraft":
                    eggid = 1
                if software == "Bungeecord":
                    eggid = 2
                if software == "Vanilla Minecraft":
                    eggid = 3
                if software == "Paper":
                    eggid = 4
                if software == "Sponge (SpongeVanilla)":
                    eggid = 5
            if category == "voice":
                nestid = 3
                if software == "Mumble Server":
                    eggid = 12
                if software == "Teamspeak3 Server":
                    eggid = 13
            if category == "discord":
                nestid = 5
                if software == "Discord JS":
                    eggid = 15
                if software == "Discord JS (typescript)":
                    eggid = 16
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
            serversCollection.insert_one({"server_name": server_name, "cpu": cpu_limit, "ram": ram, "storage": storage, "email": email})
            filter = {'email': email}
            newValues = { "$set": { 'cpu_limit': cpu_limit_db, 'memory_limit': ram_limit_db, 'server_limit': server_limit_db, 'storage_limit': storage_limit_db}}
            usersCollections.update_one(filter, newValues)
            try:
                utils.server.create_server(server_name, user_id, nestid, eggid, ram, storage, location_ids, cpu_limit, description)
                flash('Success: Server created successfully!', 'success')
                return redirect(url_for('dashboard.dashboard'))
            except:
                flash('Error: There was an issue when creating the server! Please contact the main developers.', 'error')
                return render_template('create_server.html')
    else:
        return redirect(url_for('discord.discord'))
    return render_template('create_server.html')