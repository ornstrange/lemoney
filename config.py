from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def read_config(filename):
    with open(filename, 'r') as conf_fs:
        return load(conf_fs, Loader=Loader)

if __name__ == '__main__':
    import pprint

    pprint.pprint(read_config('lemoney.yaml'))

