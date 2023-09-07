from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, blueprints
from datetime import timedelta
import os
import config
import importlib
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECERT_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
# Get a list of all files in the blueprints folder
blueprint_folder = "blueprints"
blueprint_files = [f for f in os.listdir(blueprint_folder) if f.endswith('.py') and not f.startswith("__")]

# Iterate through the blueprint files and register them
for blueprint_file in blueprint_files:
	# Import the blueprint module dynamically
	module_name = f'{blueprint_folder}.{blueprint_file[:-3]}' # Removes the .py extenstion
	blueprint_module = importlib.import_module(module_name)
    
	# Assuming each blueprint is named "bp" inside the module.
	if hasattr(blueprint_module, 'bp'):
		app.register_blueprint(blueprint_module.bp)
		print("Loaded a blueprint")

@app.errorhandler(404)
def not_found(error):
	return render_template('404.html')

@app.errorhandler(500)
def internal_error(error):
	return render_template('500.html')

if __name__ == "__main__":
	app.run(debug=True, port=5000)