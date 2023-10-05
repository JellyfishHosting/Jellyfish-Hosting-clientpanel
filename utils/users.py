from pydactyl import PterodactylClient
from directadmin.api import API
from config import pterodactyl_secert, pterodactyl_uri, directadmin_password
directadmin_api = API(username="jellyfis", password=directadmin_password, server="https://d3.my-control-panel.com:2222")
api = PterodactylClient(pterodactyl_uri, pterodactyl_secert)
def create_user(username, email, password):
    """
    Creates a new user on the Pterodactyl panel.
    
    Args:
      username (str): The username for the new user.
      email (str): The email address for the new user.
      password (str): The password for the new user.
      
    Returns:
      None
    """
    api.user.create_user(username=username, email=email, first_name="a", last_name="user", password=password, root_admin=False, language="en")

def list_users_with_email(email):
    """
    Lists all users with a given email address on the Pterodactyl panel.
    
    Args:
      email (str): The email address to search for.
      
    Returns:
      list: A list of user objects matching the email address.
    """
    result = api.user.list_users(email=email)
    return result

def update_user(email, password):
    """
    Updates a user's password on the Pterodactyl panel.
    
    Args:
      email (str): The user's email address.
      password (str): The new password.
      
    Returns:
      dict: The API response from updating the user.
    """
    data = list_users_with_email(email)
    userid = data[0]['attributes']['id']
    username = data[0]['attributes']['username']
    result = api.user.edit_user(user_id=userid, password=password, email=email, username=username, first_name="a", last_name="user")

def directadmin_create(username, email, password, domain, package, ip="198.251.84.110", notify="yes"):
    """
    Creates a new DirectAdmin user account.
    
    Args:
      username (str): The username for the account.
      email (str): The email address for the account.
      password (str): The password for the account.
      domain (str): The domain name for the account.
      package (str): The account package name.
      ip (str): Optional IP address to assign.
      notify (str): Whether to send account details to email.
      
    Returns:
      str: The API response from creating the account.
    """
    result = directadmin_api.cmd_api_account_user(
        action='create',
        add='Submit',
        username=username,
        email=email,
        passwd=password,
        passwd2=password,
        domain=domain,
        package=package,
        ip=ip,
        notify=notify
    )
    return result