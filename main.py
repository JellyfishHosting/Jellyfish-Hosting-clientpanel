from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, blueprints
from blueprints.index import index_blueprint
from blueprints.discord import discord_blueprint
from blueprints.discord_callback import discord_callback_blueprint
from blueprints.dashboard import dashboard_blueprint
from blueprints.create_server import create_server_blueprint
from blueprints.user import user_blueprint
from blueprints.create_ticket import create_ticket_blueprint
from blueprints.view_ticket import view_ticket_blueprint
from blueprints.list_tickets import list_tickets_blueprint
from blueprints.handle_ticket import handle_ticket_blueprint
from blueprints.maintenance import maintenance_blueprint
from blueprints.admindashboard import admin_dashboard_blueprint
import config
app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
app.register_blueprint(index_blueprint)
app.register_blueprint(discord_blueprint)
app.register_blueprint(discord_callback_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(create_server_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(create_ticket_blueprint)
app.register_blueprint(view_ticket_blueprint)
app.register_blueprint(list_tickets_blueprint)
app.register_blueprint(handle_ticket_blueprint)
app.register_blueprint(maintenance_blueprint)
app.register_blueprint(admin_dashboard_blueprint)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')

if __name__ == "__main__":
    app.run(port=7000, debug=True)