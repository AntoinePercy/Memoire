from benchmark import fill_random, benchmark
from server_call import what_next, add_data
from time import sleep
import sys 

num = 2
bs = "4096"
bs_int = 4096

def get_seek(bs_int) : 
	thress = 4096
	if bs_int >=thress :
		return(1)
	else :
		return( thress // bs_int)
		
		
def test_process(disk, uuid, N, data_written, size_in_blocks) :
	j = N
	seek = get_seek(bs_int)
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
				test_data["test_data"] = str({i : size_in_blocks / delay })
				test_data["data_written"] = 1 
				test_data["error"] = ""
				add_data(uuid, test_data)
				sleep(60)
				if(t==5) :
					sleep(120)
				t += 1
		result = benchmark(disk, size_in_blocks, i, count, bs, seek)
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
			
		return({"test_data" : str(test_data), "data_written" : data_written, "error": text})

	
def wait_process(uuid) :
	while True : 
		print("wait_process start")
		status = what_next(uuid)
		if( status != None ):
			if(status["in_test"]) :
				print("launch_process") 
				sys.stdout.flush()
				return(status)
		sleep(120)
		
