from pydactyl import PterodactylClient
from config import pterodactyl_secert, pterodactyl_uri
api = PterodactylClient(pterodactyl_uri, pterodactyl_secert)

def get_node_details(nodeid):
    result = api.nodes.get_node_details(nodeid)
    return result