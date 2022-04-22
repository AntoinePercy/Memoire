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

wait = True
wait_between = True
with_benchmark = True
try : 
	w = sys.argv[2]
	if w=="1" : 
		wait = False
	elif w=="2":
		wait = False
		wait_between = False
except Exception as e : 
	print(e)
	pass
	
try : 
	w = sys.argv[3]
	if w=="0" : 
		with_benchmark = False
		
except Exception as e : 
	print(e)
	pass
	
print("wait=", wait)

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
			res =  {"test_data" : "start", "data_written" : 0, "error": ""}
			add_data(uuid, res) 
			
	status = wait_process(uuid) 
	if(status["in_test"]) :
		result = test_process(disk, uuid, status["N"], status["data_written"], size_in_blocks, wait=wait, with_benchmark=with_benchmark)
		if(result != None) : 
			add_data(uuid, result)
	status = None
	wacht(120, wait_between)
	if(i == 4) : 
		wacht(1800, wait_between)
		res = {"test_data" : "hybernation", "data_written" : 0, "error": ""}
		add_data(uuid, res) 
		print("hybernation")
		i = -1
	i += 1
	



