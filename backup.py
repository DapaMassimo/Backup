# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 14:48:14 2021

@author: Massimo
"""

import sys
import os
import datetime
from decouple import config

# create name of backup folder
backup_folder = datetime.datetime.now().isoformat(' ').split(' ')[0]
backup_folder_mysql = backup_folder + "\\MySQL"

# set up backup directory
backup_dir = os.path.expanduser("~\\Desktop") + '\\' + backup_folder + '\\'
backup_dir_mysql = os.path.expanduser("~\\Desktop") + '\\' + backup_folder_mysql + '\\'

# create backup directory
try:
    os.makedirs(backup_dir)
except FileExistsError:
    print('Couldn\'t create directory: FileExistsError')
    sys.exit(1)

os.makedirs(backup_dir_mysql)

# Get enviromental variables
# MySQL config
path_to_mysql_cnf = config('mysql_config_file').replace("\"", "")
# Databases
db_list = config('databases').replace("\"", "").replace(" ", "")
db_list = db_list[1:-1].split(",")
# Folders
folders_base_path = config('folders_base_path').replace("\"", "")
folders_list = config('folders').replace("\"", "").replace(" ", "")[1:-1].split(",")


print(f"\nList of databases to backup: {db_list}\n")
for db in db_list:
    file_name = f"{backup_dir_mysql}{db}.sql"
    command = f"mysqldump --defaults-file={path_to_mysql_cnf} -u root {db} > {file_name}"
    os.system(command)

print("\n\n")
print(f"\nList of folders to backup: {folders_list}\n")
for folder in folders_list:
    ans = input(f"Do you wanna save the \'{folder}\' folder? (Y/n) ")
    if ans in ["y", "Y", "yes", "Yes", "YES"]:
        print(f"Saving the \'{folder}\' folder...\n")
        dir_to_save = folders_base_path
        command = f"cp -r {dir_to_save}{folder} {backup_dir}"
        os.system(command)
