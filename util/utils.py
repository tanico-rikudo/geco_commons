import joblib
import os, socket
import yaml
import sys

def loadJbl(filepath):
    """Loadd jbl files

    Args:
        filepath (str): target 

    Returns:
        var: loaded data 
    """
    with open(filepath, mode="rb") as f:
        data = joblib.load(f)
    return data

def saveJbl(data, filepath):
    makedirs(filepath)
    with open(filepath, mode="wb") as f:
        joblib.dump(data, f)
    return 

def load_config(path, default_path):
    path = default_path if path is None else path
    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')
    return config

def load_yaml(path):
    try:
        with open('sample.yaml') as file:
            obj = yaml.safe_load(file)
        return obj
    except Exception as e:
        print('Exception occurred while loading YAML...', file=sys.stderr)
        print(e, file=sys.stderr)
        return None

def get_env():
    info = {}
    info['hostname'] = socket.gethostname()
    if info['hostname'] in ['Macico']:
        env_name = 'DEV'
    else:
        env_name = None
    info['env_name']=env_name
    return info

def is_type(obj, _type):
    if type(obj) == _type:
        return True
    else:
        return False
    
def makedirs(path):
    dirpath=os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)