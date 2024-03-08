import os
from config import app_config

user_home = os.path.expanduser("~")
game = app_config.get('misc', 'game')
game_folder = 'Commandos' if game == 'BEL' else 'CommandosMissionPack'

# Specify the relative path to your file from the user's home directory
relative_save_file_path = f'Documents\Pyro Studios\{game_folder}\OUTPUT\REDTMP'

# Construct the full path
save_file_path = os.path.join(user_home, relative_save_file_path)
