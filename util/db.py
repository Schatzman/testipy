
import os
import subprocess
import sys

def create_db(filename):
    _file = open(filename,'w+')
    _file.close()

def delete_db(filename):
    create_db(filename)
    os.remove(filename)
