#! /usr/bin/python3
from time import time, sleep
import sys 
from server_call import *
import psutil
import os 
import subprocess

def get_disk_uuid(disk) : 
	x = disk.split("/")
	"""
	cmd = "ls"
	temp = subprocess.Popen([cmd, "-l", "/dev/disk/by-uuid"], stdout = subprocess.PIPE) 
	output, err = temp.communicate()
	"""
	cmd = "blkid"
	temp = subprocess.Popen([cmd], stdout = subprocess.PIPE) 
	output, err = temp.communicate()
	output = output.decode("utf-8")
	output = output.split("\n")
	for line in output : 
		if x[2] in line :
			return(line.split(" ")[1])
	
	return(None)

uuid = sys.argv[1]
add_usb(uuid, 1)

disk = {}
disk["sda"] = get_disk_uuid("/dev/sda")
disk["sdb"] = get_disk_uuid("/dev/sdb")
disk["sdc"] = get_disk_uuid("/dev/sdc")
disk["sdd"] = get_disk_uuid("/dev/sdd")
res = {"test_data" : str(disk), "data_written" : 0, "error": ""}
add_data(uuid, res)





while True : 
	cpu_usage = {}
	for i in range(20) : 
		cpu1, cpu5, cpu15 = psutil.getloadavg()
		cpu_usage[str(time.time())] = cpu1 / psutil.cpu_count() * 100
		sleep(60)
	res = {"test_data" : str({"cpu" : cpu_usage}), "data_written" : 0, "error": ""}
	add_data(uuid, res)
