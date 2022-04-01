from benchmark import fill_random, benchmark
from server_call import what_next, add_data
from time import sleep
import sys 

def test_process(disk, uuid, N, data_written, size_in_blocks) :
	count = int(size_in_blocks // 131072 - 1)
	if(N > 3) : 
		for i in range(data_written, data_written+N-3) :
			test_data = {}
			print("fill random number", i)
			sys.stdout.flush()
			delay = fill_random(disk, count)
			test_data["test_data"] = str({i : size_in_blocks / delay })
			test_data["data_written"] = 1 
			test_data["error"] = ""
			add_data(uuid, test_data)
	result = benchmark(disk, size_in_blocks, i, count)
	return({ "test_data" : str(result), "data_written" : 3, "error": ""})
	
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
		
