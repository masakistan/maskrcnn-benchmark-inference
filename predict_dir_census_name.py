'''
usage: <config> <input_dir> <output_dir>
'''

from maskrcnn_benchmark.config import cfg
from predictor import COCODemo
from skimage import io, color
import matplotlib.pyplot as plt
import sys, math
import torch
import numpy as np
import cv2
from collections import Counter
from os import makedirs
from os import listdir
from os.path import isfile, join
from census_name import process, cats

BUFFER = 15

config_file = sys.argv[1]

# update the config options with the config file
cfg.merge_from_file(config_file)
# manual override some options
cfg.merge_from_list(["MODEL.DEVICE", "cpu"])

coco_demo = COCODemo(
    cfg,
    confidence_threshold=0.7,
)
# load image and then run prediction

mypath = sys.argv[2]
img_paths = [(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f)) and (f[-3:] == 'jpg' or f[-3:] == 'png' or f[-3:] == 'jp2')]

out_dir = sys.argv[3]
debug_dir = sys.argv[4]
success = 0
failure = 0
skip = ['00001', '00002', '00003', '00004', '00005']

for img_idx, img_path in enumerate(img_paths):
    print(img_path)
    print("{}/{} Processing image {}".format(img_idx, len(img_paths), img_path[-1]))
    img_id = img_path[-1][img_path[-1].rfind('_') + 1: img_path[-1].rfind('.')]
    if img_id in skip:
        print('\tSkipping')
        continue

    res = process(coco_demo, img_idx, img_path, out_dir, debug_dir)
    if res is None:
        print("\tINFO: no valid cells found.")
        continue
        if res is None:
            success += 1
            continue
        status, top_predictions, predictions = res
        if status:
            success += 1
        else:
            failure += 1

    status, top_predictions, predictions = res
    #opath = join(out_dir, img_path[-1])
    #cv2.imwrite(opath, predictions)

print("Success: {}".format(success))
print("Failure: {}".format(failure))
