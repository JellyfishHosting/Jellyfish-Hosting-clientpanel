from pydactyl import PterodactylClient
from config import pterodactyl_secert, pterodactyl_uri

"""
User management module for Pterodactyl API.

Functions:

create_user(username, email, password):
  - Creates a new user on the Pterodactyl panel via the API.

list_users_with_email(email):
  - Lists users matching the given email on the Pterodactyl panel via the API.

update_user(email, password):
  - Updates the password for the user with the given email on the Pterodactyl panel via the API.
"""

api = PterodactylClient(pterodactyl_uri, pterodactyl_secert)

def create_user(username, email, password):
    api.user.create_user(username=username, email=email, first_name="a", last_name="user", password=password, root_admin=False, language="en")

def list_users_with_email(email):
    result = api.user.list_users(email=email)
    return result

def update_user(email, password):
    data = list_users_with_email(email)
    userid = data[0]['attributes']['id']
    username = data[0]['attributes']['username']
    result = api.user.edit_user(user_id=userid, password=password, email=email, username=username, first_name="a", last_name="user")
