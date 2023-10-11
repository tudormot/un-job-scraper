# import yaml
import argparse

# dir_path = os.path.dirname(os.path.realpath(__file__))
# try:
#     f = open(os.path.join(dir_path, 'config.yaml'), 'r')
# except IOError:
#     pass
# args = yaml.load(f)
# f.close()

parser = argparse.ArgumentParser(description='repository some un jobs ;)')
parser.add_argument('--chrome_version', required=False,
                    help='A specific version of chrome to be used. If not, '
                         'the latest version will be used. (note, if you do '
                         'not specify this, program assumes that latest '
                         'google chrome is installed on the machine)')
parser.add_argument('--adblocker_dir', required=False,
                    help='To be used with github actions, in order to '
                         'specify a custom dir where adblocker resides')
parser.add_argument('--db_dir', required=False,
                    help='To be used with github actions, in order to '
                         'specify a custom dir where the database should '
                         'reside. this directory should be cached with '
                         'github action')

args = parser.parse_args()
