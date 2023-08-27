from pydactyl import PterodactylClient
api = PterodactylClient('http://149.102.148.225/', 'ptla_oOM44PX5bryFwSEl9rUS8Xm91S0Dzeq5IAFs88Ll0RA')

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