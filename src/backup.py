import os
import shutil
import time

list_of_files = os.listdir('/clash-tracker/backups/')
full_path = ["/clash-tracker/backups/{0}".format(x) for x in list_of_files]

if len(list_of_files) >= 15:
    oldest_file = min(full_path, key=os.path.getctime)
    os.remove(oldest_file)
shutil.copyfile('/var/www/html/clash.json', '/clash-tracker/backups/'+str(int(time.time()))+'.clash.json')
