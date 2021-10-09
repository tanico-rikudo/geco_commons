import joblib
import os, socket

def loadJbl(filepath):
    """Loadd jbl files

    Args:
        filepath ([type]): [description]

    Returns:
        [type]: [description]
    """
    with open(filepath, mode="rb") as f:
        data = joblib.load(f)
    return data

def readJbl(data, filepath):
    with open(filepath, mode="wb") as f:
        joblib.dump(data, f)
    return 
def get_env():
    info = {}
    info['hostname'] = socket.gethostname()
    if info['hostname'] in ['Macico']:
        env_name = 'DEV'
    else:
        env_name = None
    info['env_name']=env_name
    return info
