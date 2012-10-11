import pickle
from parser import *
import re

relative_path = 'pickled_files/'

filenames = [
    '404100070.pickle',
    '454975334.pickle'
]


def extract_file(filename):
    with open(relative_path + filename) as fo:
        d = pickle.load(fo)
        new_description = remove_breaks(d['description'])
        return (new_description, d['appid'])

def remove_breaks(description):
    return re.sub('<br\s*/>', '\n', description)

if __name__ == '__main__':
   for filen in filenames:
       extract_file(filen)
