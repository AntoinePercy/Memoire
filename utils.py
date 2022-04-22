from time import sleep
import sys 

dev = False

def put_dev(devi) :
	dev = devi
	print("dev =", dev)


def wacht(t, wait=True) :  
	if(wait) :
		sleep(t)
	return()
