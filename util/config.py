import logging
import os, sys
import configparser

from  .utils import *

class ConfigManager:
    def __init__(self,config_dir):
        self.config_dir = config_dir
        self.default_config_file = {
            "general":"config.ini",
            "model":"model_config.ini",
            "private_api":"private_api.ini",
            "mongo":"mongo_config.ini",
            "log":"log_config.ini",
            "hparams":"hparams.yaml",
            "postgres":"postgres_config.ini"
        }
        
    def load_ini_config(self, path=None,config_name=None,mode=None):
        # config_ini = configparser.SafeConfigParser(os.environ) # Note: Inject Local envs to config ini file 
        config_ini = configparser.ConfigParser(os.environ) # Note: Inject Local envs to config ini file 
        path = os.path.join(self.config_dir, self.default_config_file[config_name] ) if path is None else path
        config_ini.read(path, encoding='utf-8')
        return config_ini if mode is None else config_ini[mode]
            
    def load_dict_config(self,dict_obj=None,mode=None):
        config_ini = configparser.ConfigParser()
        config_ini.read_dict(dict_obj)
        return config_ini if mode is None else config_ini[mode]
    
    def load_log_config(self,log_path,log_name):
        log_config_path= os.path.join(self.config_dir ,self.default_config_file["log"])
        logging.config.fileConfig(log_config_path,defaults={'logfilename': log_path})
        logger= logging.getLogger(log_name)
        logging.info("[DONE] Get logger. Config={0}, Log={1}".format(log_config_path, log_path))
        print(f"Log path = {log_path}")
        return logger
    
    def load_yaml_config(self, path=None, config_name=None, mode=None):
        path = os.path.join(self.config_dir, self.default_config_file[config_name] ) if path is None else path
        config = load_yaml(path)
        return config['model'][mode]['hyperparameters']
        
        
        