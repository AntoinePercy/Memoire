#! /usr/bin/python3

from benchmark import benchmark 
from get_disk_info import *
from server_call import *
from time import sleep
from test_process import test_process, wait_process
import sys

disk = sys.argv[1]
uuid_prev = 1
uuid = 0
authenticated = False
print("start of testing for disk", disk)
sys.stdout.flush()
while(True) : 
	uuid_prev = uuid
	uuid = get_disk_uuid(disk)
	print("uuid =", uuid)
	sys.stdout.flush()
	while( uuid == None) : 
			sleep(60)
			authenticated = False
			uuid = get_disk_uuid(disk)
			
	if(uuid != uuid_prev) : 
		print("change of disk")
		authenticated = False
	
	size_in_blocks = float(get_disk_info(disk))
	
	while (authenticated == False) : 
		authenticated = add_usb(uuid, size_in_blocks)
		print("authenticated =", authenticated)
		sys.stdout.flush()
		if(authenticated == False) :
			sleep(60)
		else : 
			print("Size of", disk, "is", size_in_blocks) 
			
	status = wait_process(uuid) 
	if(status["in_test"]) :
		result = test_process(disk, uuid, status["N"], status["data_written"], size_in_blocks)
		if(result != None) : 
			add_data(uuid, result)
	status = None
	sleep(120)



