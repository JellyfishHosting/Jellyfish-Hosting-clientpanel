from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, blueprints
from datetime import timedelta, datetime
import os
import importlib
import schedule
import time
import config
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
import flask_pymongo
app = Flask(__name__)
sg = sendgrid.SendGridAPIClient(config.sendgrid_api_key)
app.config['SECRET_KEY'] = config.client_secret                                     # Sets the sessions secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)                    # Sets the cookie / session lifetime to 30 minutes. Meaning every 30 minutes your cookies for this site clears.
# Get a list of all files in the blueprints folder
blueprint_folder = "blueprints"
blueprint_files = [f for f in os.listdir(blueprint_folder) if f.endswith('.py') and not f.startswith("__")]
mongodb_client = flask_pymongo.pymongo.MongoClient(config.mongo_uri)
mydb = mongodb_client['jellyfishhost']

# Iterate through the blueprint files and register them
for blueprint_file in blueprint_files:
    # Import the blueprint module dynamically
    module_name = f'{blueprint_folder}.{blueprint_file[:-3]}'                       # Removes the .py extension
    blueprint_module = importlib.import_module(module_name)

    # Assuming each blueprint is named "bp" inside the module.
    if hasattr(blueprint_module, 'bp'):
        app.register_blueprint(blueprint_module.bp)
        print("Loaded a blueprint")

def check_renewal_dates():
    current_date = datetime.now().date()
    serversCollection = mydb['servers']
    matching_servers = serversCollection.find()

    for server in matching_servers:
        renewal_date_str = server['renewal_date']
        renewal_date = datetime.strptime(renewal_date_str, '%Y-%m-%d').date()

        if renewal_date == current_date:
            email = server['email']
            from_email = Email('no-reply@jellyfishhosting.xyz')
            to_email = To(email)
            subject = "Jellyfish Hosting - Your server has been suspended!"
            content = Content('text/html', f'<p>Your server has been suspended for the reason: Failure to renew server before the due date.</p><p>Please contact our administrators by click <a href="https://my.jellyfishhosting.xyz/create_ticket">here</a> if you think this is a mistake</p><p>Kind Regards,</p><p>Jellyfish Hosting</p>')
            mail = Mail(from_email, to_email, subject, content)
            mail_json = mail.get()
            response = sg.client.mail.send.post(request_body=mail_json)
        else:
            continue

schedule.every(24).hours.do(check_renewal_dates)

# Only executes when the 404 error is catched. (Page not Found)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')                                             # Renders the 404 template in the templates folder.

# Only executes when the 500 error is catched. (Internal Server Error)
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')                                             # Renders the 500 template in the templates folder


if __name__ == "__main__":
    schedule.run_pending()
    app.run(debug=True, port=5000)