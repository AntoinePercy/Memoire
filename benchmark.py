import subprocess
import time
import numpy
import sys

#Fonctionne
def hdparm(disk) :
	cmd = 'hdparm'
	speed = []
	for i in range(50) : 
		temp = subprocess.Popen([cmd, '-t', disk], stdout = subprocess.PIPE)
		output = str(temp.communicate())
		k = output.find("MB/sec")
		speed.append(float(output[k-6:k-1]))
	speed = numpy.array(speed)
	return(numpy.mean(speed))


#Function that fill the disk of one this is the erase operation
def fill_1(disk, count):
	print("fill one start")
	cmd = 'pv'
	print("disk = {}".format(disk))
	start = time.time()
	temp = subprocess.run(["tr '\0' '\377' < /dev/zero | dd bs=128K seek=1 count={} of={}".format(count ,disk)], shell = True, universal_newlines = True, capture_output=True)
	output = temp.stderr
	stop = time.time()
	return(stop - start)


#function that fill the disk of zero return the total time of the write.
def fill_0(disk, count):
	print("fill zero start")
	cmd = "dd"
	start = time.time()
	temp = subprocess.Popen([cmd, "if=/dev/zero", "of={}".format(disk), "bs=128K", "count={}".format(count), "seek=1"], stdout = subprocess.PIPE)
	temp.wait()
	stop = time.time()
	return(stop-start)
	
def fill_random(disk, count):
	return(234141)
	print("fill random start")
	sys.stdout.flush()
	cmd = "dd"
	start = time.time()
	temp = subprocess.Popen([cmd, "if=/dev/random", "of={}".format(disk), "bs=128K", "count={}".format(count), "seek=1"], stdout = subprocess.PIPE)
	temp.wait()
	stop = time.time()
	return(stop-start)
	
def erase_after_random(disk, count) : 
	fill_time = fill_random(disk, count)
	erase_time = fill_1(disk, count)
	
def zero_after_one(disk) : 
	fill_one = fill_1(disk, count)
	fill_zero = fill_0(disk, count)
	
def one_after_zero(disk) :
	fill_zero = fill_0(disk, count)
	fill_one = fill_1(disk, count)
	 

def benchmark(disk, size_in_blocks, N, count) : 
	#read_test = hdparm(disk)
	print("count", count)
	fill_0_test = size_in_blocks / fill_0(disk, count) 
	#fill_random_test = size_in_blocks / fill_random(disk, count) 
	#fill_1_test = size_in_blocks / fill_1(disk, count)
	return({"fill_0_test" : fill_0_test,
			"fill_1_test" : fill_1_test,
			"read_test" : read_test, 
			"fill_random" : fill_random_test
			})
