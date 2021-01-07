import yaml

try:
    f = open('config.yaml', 'r')
except IOError:
    pass
args = yaml.load(f)
f.close()

if __name__ == '__main__':
    print(args['program_behaviour'])
