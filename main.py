#! /usr/bin/python3

from benchmark import benchmark 
from get_disk_info import *
from server_call import *
from utils import wacht, put_dev
from test_process import test_process, wait_process
import sys

disk = sys.argv[1]
uuid_prev = 1
uuid = 0
authenticated = False
print("start of testing for disk", disk)
sys.stdout.flush()

try : 
	put_dev(sys.argv[2])
except Exception as e : 
	print(e)
	pass


i = 0
while(True) : 
	uuid_prev = uuid
	uuid = get_disk_uuid(disk)
	print("uuid =", uuid)
	sys.stdout.flush()
	while( uuid == None) : 
			wacht(60)
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
			wacht(60)
		else : 
			print("Size of", disk, "is", size_in_blocks) 
			
	status = wait_process(uuid) 
	if(status["in_test"]) :
		result = test_process(disk, uuid, status["N"], status["data_written"], size_in_blocks)
		if(result != None) : 
			add_data(uuid, result)
	status = None
	wacht(120)
	if(i == 5) : 
		wacht(1800)
		print("hybernation")
		i = 0
	i += 1
	



