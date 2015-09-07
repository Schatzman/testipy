## UTILS
import datetime
import logging
import sys
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(levelname)s] %(asctime)s (%(threadName)-10s) %(message)s',
        )
    return logging

def read_yaml(filename_yaml):
    stream = open(filename_yaml, 'r')
    data = yaml.load(stream, Loader=Loader)
    return data

def str_utcnow():
    strft_str = "%A, %B %d, %Y - %H:%M:%S:%f UTC"
    now = datetime.datetime.utcnow()
    return now.strftime(strft_str)

def up_one_dir():
    if sys.platform == 'win32':
        sys.path.append('..\\')
    elif sys.platform == 'darwin':
        sys.path.append('../')
    else:
        print("Hmmm.... unknown platform. What is %s?" % sys.platform)
