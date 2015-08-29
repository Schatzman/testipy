import os
import subprocess
import sys

def create_db(filename):
    _file = open(filename, 'w+')
    _file.close()

def delete_db(filename):
    create_db(filename)
    if sys.platform == 'win32':
        subprocess.call(["del",filename],shell=True)
    elif sys.platform == 'darwin':
        os.remove(filename)
    else:
        print("Unknown platform: %s!" % sys.platform)