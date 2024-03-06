from configparser import ConfigParser


class AppConfig:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
    

    def get(self, section, key):
        return self.config.get(section, key)


    def set(self, section, key, value):
        self.config.set(section, key, value)
        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)


app_config = AppConfig()
