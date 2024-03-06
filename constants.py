import os

user_home = os.path.expanduser("~")

# TODO: Add support for BCD path
# Specify the relative path to your file from the user's home directory
relative_save_file_path = "Documents\Pyro Studios\Commandos\OUTPUT\REDTMP"

# Construct the full path
save_file_path = os.path.join(user_home, relative_save_file_path)
