## UTILS
import logging
import sys
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
def up_one_dir():
    if sys.platform == 'win32':
        sys.path.append('..\\')
    elif sys.platform == 'darwin':
        sys.path.append('../')
    else:
        print("Hmmm.... unknown platform. What is %s?" % sys.platform)
up_one_dir()

def read_yaml(filename_yaml):
    stream = open(filename_yaml, 'r')
    data = yaml.load(stream, Loader=Loader)
    return data

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] %(asctime)s (%(threadName)-10s) %(message)s',
        )