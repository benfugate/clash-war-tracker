import os
import shutil
import time
from config import Config

config = Config()

backup_dir = f'{config.storage_folders}/backups/'
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

list_of_files = os.listdir(backup_dir)
full_path = ["{0}/{1}".format(backup_dir, x) for x in list_of_files]

if len(list_of_files) >= 15:
    oldest_file = min(full_path, key=os.path.getctime)
    os.remove(oldest_file)
shutil.copyfile(config.clash_json, f'{backup_dir}/{str(int(time.time()))}.clash.json')
