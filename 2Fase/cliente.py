import http.client
import threading
import sys


def cli():
	BODY = ""
	conn = http.client.HTTPConnection("127.0.0.1", 80)
	conn.request("GET", "/file1", BODY)
	response = conn.getresponse()
	#print(response)#, response.reason)
	print("\nCliente1\n",response.read(200))
	  

def cli2():
	BODY = "***filecontents***"
	conn = http.client.HTTPConnection("127.0.0.1", 80)
	conn.request("GET", "/", BODY)
	response = conn.getresponse()
	#print(response)#, response.reason)
	print("\nCliente2\n",response.read(200))
	  



for x in range(0,10):
	y=threading.Thread(target=cli, args=())
	y2=threading.Thread(target=cli2, args=())
	y.start()
	y2.start()