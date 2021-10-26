import flask



VPS_IP_ADDRESS = '104.225.208.116'


def isProductionEnv() -> bool:

    server_ip, server_port = flask.request.server

    if server_ip == VPS_IP_ADDRESS:
        return True
    else:
        return False

    
    
