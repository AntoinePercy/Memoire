import requests
import urllib
import json
import time

endpoint = "https://us-central1-usb-data.cloudfunctions.net/usb"

#fontionne
def add_usb(uuid, size) :
	try : 
		url = "{}/add_usb/{}".format(endpoint, uuid)
		print("url =", url)
		payload='size={}'.format(size)
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		response = requests.request("POST", url, headers=headers, data=payload)
		if(response.status_code == 201) : 
			return(True) 
		else : 
			return(False)
	except Exception as e : 
		print(e)
		time.sleep(300)
		return(add_usb(uuid, size))
		
#fonctionne	sans la gestion des erreurs
def what_next(uuid) :
	try : 
		url = "{}/what_next/{}".format(endpoint, uuid)

		payload={}
		headers = {}
		response = requests.request("GET", url, headers=headers, data=payload)
		if(response.status_code == 200):
			return(response.json())
		else : 
			return(None)
	except Exception as e : 
		print(e)
		time.sleep(300)
		return(what_next(uuid))

#fonctionne sans la gestion des erreurs		
def add_data(uuid, data) :
	try :
		while(True) :
			url = "{}/add_data/{}".format(endpoint, uuid)
			payload = data
			print(data)
			headers = {
			  'Content-Type': 'application/x-www-form-urlencoded'
			}

			response = requests.request("POST", url, headers=headers, data=payload)
			if(response.status_code == 201) : 
				return(response.json())
			else :
				print(response.status_code)
				time.sleep(60)
	except Exception as e : 
		print(e)
		time.sleep(300)
		return(add_data(uuid, data))

		
