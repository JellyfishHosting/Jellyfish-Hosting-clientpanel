from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, blueprints
from datetime import timedelta
import os
import importlib
import config
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY                                        # Sets the sessions secret_key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)                    # Sets the cookie / session lifetime to 30 minutes. Meaning every 30 minutes your cookies for this site clears.
# Get a list of all files in the blueprints folder
blueprint_folder = "blueprints"
blueprint_files = [f for f in os.listdir(blueprint_folder) if f.endswith('.py') and not f.startswith("__")]

# Iterate through the blueprint files and register them
for blueprint_file in blueprint_files:
    # Import the blueprint module dynamically
    module_name = f'{blueprint_folder}.{blueprint_file[:-3]}'                       # Removes the .py extension
    blueprint_module = importlib.import_module(module_name)

    # Assuming each blueprint is named "bp" inside the module.
    if hasattr(blueprint_module, 'bp'):
        app.register_blueprint(blueprint_module.bp)
        print("Loaded a blueprint")

# Only executes when the 404 error is catched. (Page not Found)
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')                                             # Renders the 404 template in the templates folder.

# Only executes when the 500 error is catched. (Internal Server Error)
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html')                                             # Renders the 500 template in the templates folder


if __name__ == "__main__":
    app.run(debug=True, port=5000)