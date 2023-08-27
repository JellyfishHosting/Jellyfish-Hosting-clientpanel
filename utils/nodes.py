from pydactyl import PterodactylClient
api = PterodactylClient('http://149.102.148.225/', 'ptla_oOM44PX5bryFwSEl9rUS8Xm91S0Dzeq5IAFs88Ll0RA')

def get_node_details(nodeid):
    result = api.nodes.get_node_details(nodeid)
    return result