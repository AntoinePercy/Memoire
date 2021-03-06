import subprocess
from utils import wacht
import numpy
import sys
import time
bs = "256K"

#Fonctionne
def hdparm(disk) :
	cmd = 'hdparm'
	speed = []
	for i in range(50) : 
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
		print(res)
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
	temp = subprocess.Popen([cmd, "if=/dev/random", "of={}".format(disk), "bs={}".format(bs), "count={}".format(count), "seek={}".format(str(seek)), "conv=fsync", "status=progress"])
	temp.wait()
	stop = time.time()
	res = temp.communicate()
	if(temp.returncode != 0) : 
		raise Exception(2,"Fill random Error with count={} and disk={}".format(count, disk))
	return(stop-start)
	
#function that fill the disk of zero return the total time of the write.
def fill_zero_direct(disk, count, bs, seek):
	print("fill zero start")
	cmd = "dd"
	start = time.time()
	temp = subprocess.Popen([cmd, "if=/dev/zero", "of={}".format(disk), "oflag=direct", "bs={}".format(bs), "count={}".format(count), "seek={}".format(str(seek))], stdout = subprocess.PIPE)
	temp.wait()
	stop = time.time()
	res = temp.communicate()
	if(temp.returncode != 0) : 
		raise Exception(1, "Fill 0 Error with count={} and disk={}".format(count, disk))
	return(stop-start)
	
def fill_random_direct(disk, count, bs, seek): 
	sys.stdout.flush()
	cmd = "dd"
	start = time.time()
	temp = subprocess.Popen([cmd, "if=/dev/random", "of={}".format(disk), "bs={}".format(bs), "oflag=dsync", "status=progress", "count={}".format(count), "seek={}".format(str(seek))])
	temp.wait()
	stop = time.time()
	res = temp.communicate()
	if(temp.returncode != 0) : 
		raise Exception(2,"Fill random Error with count={} and disk={}".format(count, disk))
	return(stop-start)

def fill_one_direct(disk, count, bs, seek):
	print("fill one start")
	cmd = "bash"
	start = time.time()
	temp = subprocess.Popen([cmd, "fill_1_direct.sh", str(count), disk, bs, str(seek)], stdout = subprocess.PIPE)
	temp.wait()
	stop = time.time()
	res = temp.communicate()
	if(temp.returncode != 0) : 
		print(res)
		raise Exception(3, "Fill 1 Error with count={} and disk={}".format(count, disk))
	return(stop - start)
	

def benchmark(disk, size_in_blocks, N, count, bs, seek) : 
	read_test = None
	fill_0_test = None
	fill_random_test = None
	fill_1_test = None
	try :
		wacht(60)
		t0 = time.time()
		read_test = hdparm(disk)
		wacht(60)
		t1 = time.time()
		fill_0_test = size_in_blocks / fill_0(disk, count, bs, seek) 
		wacht(60)
		t2 = time.time()
		fill_random_test = size_in_blocks / fill_random(disk, count, bs, seek) 
		wacht(60)
		t3 = time.time()
		fill_1_test = size_in_blocks / fill_1(disk, count, bs, seek)
		wacht(60)
		return({"fill_0_test" : fill_0_test,
				"fill_1_test" : fill_1_test,
				"read_test" : read_test, 
				"fill_random" : fill_random_test,
				"t0" : t0,
				"t1" : t1,
				"t2" : t2,
				"t3" : t3
				})
	except Exception as e :
		case , text  = e.args
		print("error", text) 
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
