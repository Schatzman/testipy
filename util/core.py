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

def convert_yml_bool(value):
	if value == 0:
		return False
	if value == 1:
		return True
	else:
		raise Exception(repr(value) + " is not == 1 (True) or 0 (False).")