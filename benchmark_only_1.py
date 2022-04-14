#! /usr/bin/python3

from benchmark import *
from get_disk_info import *
from test_process import get_seek
import numpy as np

disk = sys.argv[1]
bs = int(sys.argv[2])
size_in_blocks = int(get_disk_info(disk))
print("size in block", size_in_blocks)
seek = get_seek(bs)
print(seek)
print("writing on disk", disk) 
count = (size_in_blocks // (bs) - 1)
delay = benchmark(disk, size_in_blocks, 10, str(count), str(bs), str(seek))
print("delay =", delay)
