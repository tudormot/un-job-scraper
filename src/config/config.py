# import yaml
import argparse

# dir_path = os.path.dirname(os.path.realpath(__file__))
# try:
#     f = open(os.path.join(dir_path, 'config.yaml'), 'r')
# except IOError:
#     pass
# args = yaml.load(f)
# f.close()

parser = argparse.ArgumentParser(description='scrape some un jobs ;)')
parser.add_argument('--adblocker_dir', required=False,
                    help='To be used with github actions, in order to '
                         'specify a custom dir where adblocker resides')

args = parser.parse_args()
