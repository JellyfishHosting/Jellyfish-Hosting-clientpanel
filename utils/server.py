from pydactyl import PterodactylClient
from config import pterodactyl_secert, pterodactyl_uri
api = PterodactylClient(pterodactyl_secert, pterodactyl_uri)

def create_server(name, user_id, nestid, eggid, ram, storage, location_ids, cpu_limit, description):
    api.servers.create_server(name=name, user_id=user_id, nest_id=nestid, egg_id=eggid, memory_limit=ram, cpu_limit=cpu_limit, description=description, swap_limit=0, backup_limit=20, database_limit=2, disk_limit=storage, location_ids=location_ids)