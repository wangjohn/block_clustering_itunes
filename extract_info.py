import pickle
from parser import *
from max_block_cover import *
import re

relative_path = 'pickled_files/'

filenames = [
    '404100070.pickle',
    #'454975334.pickle'
]


def extract_file(filename):
    with open(relative_path + filename) as fo:
        d = pickle.load(fo)
        new_description = remove_breaks(d['description'])
        return (new_description, d['appid'])

def remove_breaks(description):
    return re.sub('<br\s*/>', '\n', description)

def get_blocks(description):
    fitness_obj = Fitness(description)
    fitness_obj.get_potential_blocks()
    max_cover_obj = MaxBlockCover(fitness_obj.potential_blocks)
    return max_cover_obj.get_max_covering()

def get_blocks_from_all_files(filenames):
    blocks_appid_hash = {}
    for filename in filenames:
       (description, appid) = extract_file(filename)
       blocks_appid_hash[appid] = get_blocks(description)
    return blocks_appid_hash

def print_out_blocks(blocks_hash):
    for (appid, list_of_blocks) in blocks_hash.iteritems():
        print 'App Id: ' + appid
        for block in list_of_blocks:
            print block
        
if __name__ == '__main__':
    blocks_hash = get_blocks_from_all_files(filenames)
    print_out_blocks(blocks_hash)
