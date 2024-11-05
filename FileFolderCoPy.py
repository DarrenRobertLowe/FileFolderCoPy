# =====================================
# Title: FileFolderCoPy
# =====================================

"""
Author: Darren Robert Lowe
Date: 2024-11-05
Description: Copies the source folder to the destination and logs the process.
"""

import os
import io
import shutil
import datetime
import sys
from timeit import default_timer as timer

def debug(message):
    print(message)
    log.write(message + "\n")

def date_directory(directory):
    return str(directory + " " + getDateTimeString())

def getDateTimeString():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def backup_directory(source, destination, onlyLogErrors):
    if os.path.exists(destination):
        debug(f"Error! Destination '{destination}' already exists! Process will not continue!")
        sys.exit(1)
    elif not os.path.exists(source):
        debug(f"Error! Source '{source}' not found! Process will not continue!")
        sys.exit(1)
    else:
        os.makedirs(destination)
        if not onlyLogErrors:
            debug(f"Created directory {destination}")
        
        try:
            for item in os.listdir(source):
                s = os.path.join(source, item)
                d = os.path.join(destination, item)
                
                try:
                    if os.path.isdir(s):
                        backup_directory(s, d, onlyLogErrors) # recursion needed for subfolder contents
                    else:
                        shutil.copy2(s, d)
                except Exception as e:
                    debug(f"Error: source: '{s}'  dest: '{d}'  : {e} \n Skipping file and continuing...")
                else:
                    if not onlyLogErrors:
                        debug(f"copied {s} to {d}")
        except Exception as e:
            debug(str(e) + " \n Skipping file and continuing...")

if __name__ == '__main__':
    startTime = timer()
    log_path = "log_" + getDateTimeString() + ".txt"
    log = io.open(log_path, 'w')
    onlyLogErrors = True #set to false to see details of every successful copy
    
    appdata = os.path.expanduser("~\\AppData")
    source_directory = appdata
    destination_directory = date_directory("E:\\BACKUPS AND STORAGE\\AppData_Backup")
    
    
    debug(f"Copying '{source_directory}' to '{destination_directory}'...")
    backup_directory(source_directory, destination_directory, onlyLogErrors)
    endTime = timer()
    debug("File copying completed. See log for any errors.")
    debug("Time taken: " + str(endTime - startTime) + " seconds.")
    log.close()
    
