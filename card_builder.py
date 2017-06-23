
# organizes files into output/card structure

import os
import re
import shutil
import math

NUM_DIRS=16

def find_all_splits(dir):
    print("Checking %s" %(dir))
    files = os.listdir(dir)
    files = filter(lambda x: re.match(r'out\d+_split_\d+.wav', x), files)
    return map(lambda x: "%s/%s" % (dir, x), sorted(files))

def create_card_dir(dir):
    if(os.path.isdir(dir)):
        shutil.rmtree(dir);
    os.mkdir(dir)
    for i in range(0, NUM_DIRS):
        numdir = "%s/%d" % (dir, i)
        print("Creating %s" % (numdir))
        os.mkdir(numdir)

def chunkify_move(split_files, card_dir):
    files_per_dir = len(split_files)/NUM_DIRS
    # TODO: check if files_per_dir > 48 (that's an err, limitation in radio music firmware)
    print("%d files per directory" % (files_per_dir))
    file_sets = [split_files[i:i+files_per_dir] for i in range(0, len(split_files), files_per_dir)]
    # distribute among output dirs -- last dir ends up with "extra" files. oh well.
    while(len(file_sets) > NUM_DIRS):
        last = len(file_sets) - 1;
        file_sets[last-1] = file_sets[last-1] + file_sets[last]
        file_sets.pop()
    print(file_sets)
    print(len(file_sets))
    outdir_num = 1
    for set in file_sets:
        outdir = "%s/%d" % (card_dir, outdir_num)
        for file in set:
            print("Copying %s to %s..." % (file, outdir))
            shutil.copy(file, outdir)
        outdir_num = outdir_num + 1

def prep_card_dir(path):
    tmpout = "%s/tmp" % (path)
    card_dir = "%s/card" % (path)
    print("Prepping card dir at %s" % (card_dir))
    create_card_dir(card_dir)
    split_files = find_all_splits(tmpout)
    print("Distributing %d files into %d card dirs..." % (len(split_files), NUM_DIRS))
    chunkify_move(split_files, card_dir)
    print("Cleaning up...")
    # shutil.rmtree(tmpout)
