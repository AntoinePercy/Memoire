from benchmark import fill_random, benchmark, fill_random_direct, fill_one_direct, fill_zero_direct
from server_call import what_next, add_data
from utils import wacht
import sys 
import time

num = 2
bs = "4096"
bs_int = 4096

def get_seek(bs_int) : 
	thress = 4096
	if bs_int >=thress :
		return(1)
	else :
		return( thress // bs_int)
		
		
def test_process(disk, uuid, N, data_written, size_in_blocks, wait=True, with_benchmark=True) :
	j = N
	seek = get_seek(bs_int)
	direct_bs = 131072
	try : 
		t = 0
		count = int(size_in_blocks // (bs_int) - 1)
		if(N > 3) : 
			for i in range(data_written, data_written+N-3) :
				j = i
				test_data = {}
				print("fill random number", i)
				sys.stdout.flush()
				delay = fill_random(disk, count, bs, seek)
				tt = time.time()
				delay_sync = 1
				delay_0 = 1
				delay_1 = 1
				if(with_benchmark) : 
					wacht(1)
					delay_sync = fill_random_direct(disk, 1, direct_bs, 1)
					wacht(1)
					delay_0 = fill_zero_direct(disk, 1, direct_bs, 2)
					wacht(1)
					delay_1 = fill_one_direct(disk, str(1), str(direct_bs), str(3))
				test_data["test_data"] = str({i : (size_in_blocks / delay), "t" : tt , "random" : (direct_bs / delay_sync),
												"one" : (direct_bs / delay_1), "zero" : ( direct_bs / delay_0) })
				test_data["data_written"] = 1 
				test_data["error"] = ""
				print("in process is test_data =", test_data)
				add_data(uuid, test_data)
				wacht(60, wait)
				if(t==5) :
					wacht(120, wait)
				t += 1
		result = {}
		if(with_benchmark) :		
			result = benchmark(disk, size_in_blocks, i, str(count), str(bs), str(seek))
		return({ "test_data" : str(result), "data_written" : 3, "error": ""})
	
	except Exception as e:
		text, test_data = e.args
		if(text == 2) : 
			text = test_data
			test_data = {j : "error"}
			data_written = 0
		else : 
			data_written = test_data["data_written"]
			test_data = test_data["test_data"]
			test_data[j+data_written] =  "error"
			
		return({"test_data" : str(test_data), "data_written" : data_written, "error": ""})

	
def wait_process(uuid) :
	while True : 
		print("wait_process start")
		status = what_next(uuid)
		if( status != None ):
			if(status["in_test"]) :
				print("launch_process") 
				sys.stdout.flush()
				return(status)
		wacht(120)
		
