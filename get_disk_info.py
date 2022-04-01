import subprocess
import re


#get uuid is working but we need that the disk is mounted
#return NULL is not working
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



def get_disk_info(disk, uuid) : 
	cmd = "blockdev" 
	temp = subprocess.Popen([cmd, "--getsize64", disk], stdout = subprocess.PIPE)
	output, err = temp.communicate() 
	if( err != None ) :
		return(None)
	return(output.decode("utf-8"))
	
	
	
