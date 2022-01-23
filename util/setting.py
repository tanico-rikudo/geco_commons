import os,sys
sys.path.append(os.path.join(os.environ['COMMON_DIR'],"util" ))
os.environ['KULOKO_DIR'] = os.path.join(os.environ['HOST_BASE_DIR'], "kuloko")
os.environ['ALEISTER_DIR'] = os.path.join(os.environ['HOST_BASE_DIR'], "aleister")
os.environ['COMMON_DIR'] = os.path.join(os.environ['HOST_BASE_DIR'], "geco_commons")
os.environ['AIWASS_DIR'] = os.path.join(os.environ['HOST_BASE_DIR'], "aiwass")

os.environ['KULOKO_INI'] = os.path.join(os.environ['COMMON_DIR'], "ini")
os.environ['ALEISTER_INI'] = os.path.join(os.environ['COMMON_DIR'], "ini")

# os.environ['LOGDIR'] = os.path.join(os.environ['KULOKO_DIR'], "log")
os.environ['KULOKO_LOGDIR'] = os.path.join(os.environ['KULOKO_DIR'] ,"log")
os.environ['ALEISTER_LOGDIR'] = os.path.join(os.environ['ALEISTER_DIR'] ,"log")
os.environ['AIWASS_LOGDIR'] = os.path.join(os.environ['AIWASS_DIR'] ,"log")
os.environ['AIWASS_LOG'] = os.path.join(os.environ['AIWASS_LOGDIR'] ,"aiwass.log")

os.environ['MONGO_DIR'] = os.path.join(os.environ['COMMON_DIR'] ,"mongodb")


# os.environ['MLFLOW_TRACKING_URI'] = os.path.join(os.environ['HOST_BASE_DIR'], "mlruns")
# OS.environ['MLFLOW_ARTIFACTS_URI'] = os.path.join(os.environ['HOST_BASE_DIR'], "mlruns")
os.environ['MLFLOW_TRACKING_URI'] = 'http://'+os.environ['MLFLOW_HOST']+':5000'
os.environ['MLFLOW_ARTIFACTS_URI'] = os.path.join(os.environ['HOST_BASE_DIR'], "mlruns")
os.environ['DEFAULT_LOCAL_FILE_AND_ARTIFACT_PATH'] = os.path.join(os.environ['HOST_BASE_DIR'], "mlruns")

sys.path.append(os.path.join(os.environ['KULOKO_DIR'],"items" ))
