import subprocess
from utils import wacht
import numpy
import sys

bs = "256K"

#Fonctionne
def hdparm(disk) :
	cmd = 'hdparm'
	speed = []
	for i in range(250) : 
		temp = subprocess.Popen([cmd, '-t', disk], stdout = subprocess.PIPE)
		#if(temp.returncode != 0) :
		#	raise Exception(0, "Fill random Error with disk={}".format(disk))
		output = str(temp.communicate())
		k = output.find("MB/sec")
		speed.append(float(output[k-6:k-1]))
	speed = numpy.array(speed)
	return(numpy.mean(speed))


#Function that fill the disk of one this is the erase operation
def fill_1(disk, count, bs, seek):
	print("fill one start")
	cmd = "bash"
	start = time.time()
	temp = subprocess.Popen([cmd, "fill_1.sh", str(count), disk, bs, str(seek)], stdout = subprocess.PIPE)
	temp.wait()
	stop = time.time()
	res = temp.communicate()
	if(temp.returncode != 0) : 
		raise Exception(3, "Fill 1 Error with count={} and disk={}".format(count, disk))
	return(stop - start)


#function that fill the disk of zero return the total time of the write.
def fill_0(disk, count, bs, seek):
	print("fill zero start")
	cmd = "dd"
	start = time.time()
	temp = subprocess.Popen([cmd, "if=/dev/zero", "of={}".format(disk), "bs={}".format(bs), "count={}".format(count), "seek={}".format(str(seek))], stdout = subprocess.PIPE)
	temp.wait()
	stop = time.time()
	res = temp.communicate()
	if(temp.returncode != 0) : 
		raise Exception(1, "Fill 0 Error with count={} and disk={}".format(count, disk))
	return(stop-start)
	
def fill_random(disk, count, bs, seek):
	sys.stdout.flush()
	cmd = "dd"
	start = time.time()
	temp = subprocess.Popen([cmd, "if=/dev/random", "of={}".format(disk), "bs={}".format(bs), "count={}".format(count), "seek={}".format(str(seek))])
	temp.wait()
	stop = time.time()
	res = temp.communicate()
	if(temp.returncode != 0) : 
		raise Exception(2,"Fill random Error with count={} and disk={}".format(count, disk))
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
	 

def benchmark(disk, size_in_blocks, N, count, bs, seek) : 
	read_test = None
	fill_0_test = None
	fill_random_test = None
	fill_1_test = None
	try :
		wacht(60)
		read_test = hdparm(disk)
		wacht(60)
		fill_0_test = size_in_blocks / fill_0(disk, count, bs, seek) 
		wacht(60)
		fill_random_test = size_in_blocks / fill_random(disk, count, bs, seek) 
		wacht(60)
		fill_1_test = size_in_blocks / fill_1(disk, count, bs, seek)
		wacht(60)
		return({"fill_0_test" : fill_0_test,
				"fill_1_test" : fill_1_test,
				"read_test" : read_test, 
				"fill_random" : fill_random_test
				})
	except Exception as e :
		case , text  = e.args 
		test_data = {}
		data_written = 0
		if(case > 0) : 
			test_data["read_test"] = read_test
		if(case > 1) : 
			test_data["fill_0_test"] = fill_0_test
			data_written += 1
		if(case > 2) : 
			test_data["fill_random_test"] = fill_random_test
			data_written += 1
		if(case > 3): 
			test_data["fill_1_test"] = fill_1_test
			data_written += 1
			
		raise Exception(text, {"test_data" : test_data, "data_written" : data_written})
