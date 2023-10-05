from pydactyl import PterodactylClient
from config import pterodactyl_secert, pterodactyl_uri
api = PterodactylClient(pterodactyl_uri, pterodactyl_secert)

def create_server(name, user_id, nestid, eggid, ram, storage, location_ids, cpu_limit, description):
    """Creates a new server on the Pterodactyl panel.
    
    Args:
      name (str): The name for the new server.
      user_id (int): The ID of the user to assign the server to.
      nestid (int): The ID of the nest for the server. 
      eggid (int): The ID of the egg to use for the server.
      ram (int): The amount of RAM to allocate to the server in MB.
      storage (int): The amount of disk space to allocate in MB.
      location_ids (list): A list of location IDs for the server.
      cpu_limit (int): The CPU limit percentage. 
      description (str): A description for the new server.
      
    Returns:
      dict: The server creation response from the API.
    """
    result = api.servers.create_server(name=name, user_id=user_id, nest_id=nestid, egg_id=eggid, memory_limit=ram, cpu_limit=cpu_limit, description=description, swap_limit=0, backup_limit=20, database_limit=2, disk_limit=storage, location_ids=location_ids)
    return result

def suspend_server(server_id):
    """Suspends a server on the Pterodactyl panel.

    Args:
    server_id (int): The ID of the server to suspend.

    Returns:
      None
    """
    api.servers.suspend_server(server_id=server_id)