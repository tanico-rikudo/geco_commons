import os,sys
os.environ['BASE_DIR'] =  '/Users/macico/Dropbox/btc'
os.environ['COMMON_DIR'] = os.path.join(os.environ['BASE_DIR'], "geco_commons")
sys.path.append(os.path.join(os.environ['COMMON_DIR'],"util" ))
os.environ['KULOKO_DIR'] = os.path.join(os.environ['BASE_DIR'], "kuloko")
os.environ['ALEISTER_DIR'] = os.path.join(os.environ['BASE_DIR'], "aleister")
os.environ['ALEISTER_INI'] = os.path.join(os.environ['COMMON_DIR'], "ini")
os.environ['COMMON_DIR'] = os.path.join(os.environ['BASE_DIR'], "geco_commons")
os.environ['KULOKO_INI'] = os.path.join(os.environ['COMMON_DIR'], "ini")
os.environ['MONGO_DIR'] = os.path.join(os.environ['COMMON_DIR'] ,"mongodb")
os.environ['LOGDIR'] = os.path.join(os.environ['KULOKO_DIR'], "log")
sys.path.append(os.path.join(os.environ['KULOKO_DIR'],"items" ))
# os.environ['MLFLOW_TRACKING_URI'] = os.path.join(os.environ['BASE_DIR'], "mlruns")
# OS.environ['MLFLOW_ARTIFACTS_URI'] = os.path.join(os.environ['BASE_DIR'], "mlruns")
os.environ['MLFLOW_TRACKING_URI'] = 'http://localhost:5000'
os.environ['MLFLOW_ARTIFACTS_URI'] = os.path.join(os.environ['BASE_DIR'], "mlruns")
os.environ['DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH'] = os.path.join(os.environ['BASE_DIR'], "mlruns")
