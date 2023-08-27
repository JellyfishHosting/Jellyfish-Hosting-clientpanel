from pydactyl import PterodactylClient
api = PterodactylClient('http://149.102.148.225/', 'ptla_oOM44PX5bryFwSEl9rUS8Xm91S0Dzeq5IAFs88Ll0RA')

def create_server(name, user_id, nest_id, egg_id, memory_limit, storage_limit, location_ids, cpu_limit, description):
    api.servers.create_server(name=name, user_id=user_id, nest_id=nest_id, egg_id=egg_id, memory_limit=memory_limit, cpu_limit=cpu_limit, description=description, swap_limit=0, backup_limit=20, database_limit=2, disk_limit=storage_limit, location_ids=location_ids)