
class ConfigManager:
    def __init__(config_dir):
        self.config_dir = config_dir
        self.default_config_file = {
            "general":"config.ini",
            "model":"model_config.ini",
            "private_api":"private_api.ini"
        }
        
    def load_ini_config(self, path=None,config_name=None,mode=None):
        config_ini = configparser.ConfigParser()
        path = os.path.join(self.config_dir, self.default_config_file[config_name] ) if path is None else path
        return config_ini.read(path, encoding='utf-8')[mode]
            
    def load_dict_config(dict_obj=None,mode=None):
        config_ini = configparser.ConfigParser()
        return parser.read_dict(dict_obj)[mode]
        
        