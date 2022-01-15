import yaml
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    f = open(os.path.join(dir_path, 'config.yaml'), 'r')
except IOError:
    pass
args = yaml.load(f)
f.close()
