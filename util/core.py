## UTILS
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def read_yaml(filename_yaml):
    stream = open(filename_yaml, 'r')
    data = yaml.load(stream, Loader=Loader)
    return data
