#! /usr/bin/python3

from benchmark import *
from get_disk_info import *
from test_process import get_seek
import numpy as np

disk = ["/dev/sda", "/dev/sdb", "/dev/sdc", "/dev/sdd"]

bs = 4096
result = {"/dev/sda" : [], "/dev/sdb" : [], "/dev/sdc" : []  , "/dev/sdd" : []}
print("start")
uuid = {}
for d in disk:
	uuid[d] = get_disk_uuid(d)
print("uuid =", uuid)
for _ in range(5) : 
	for d in disk : 
		size_in_blocks = int(get_disk_info(d))
		print("size in block", size_in_blocks)
		seek = get_seek(bs)
		print(seek)
		print("writing on disk", d) 
		count = (size_in_blocks // (bs) - 2)
		res = fill_random(d, count, bs, seek) 
		print(d, res) 
		result[d].append(res)
		print(uuid, result)
	
print(uuid, result)

mean = {}
for disk, tab in result.items() : 
	nptab = np.array(tab)
	mean[disk] = np.mean(nptab)

print(uuid, mean)
	
	
