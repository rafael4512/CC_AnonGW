import http.client
import threading
import sys
def cli():
	BODY = "***filecontents***"
	conn = http.client.HTTPConnection("localhost", 80)
	conn.request("GET", "/file1", BODY)
	response = conn.getresponse()
	#print(response)#, response.reason)
	print(response.read(200))
	  


for x in range(0,20):
	y=threading.Thread(target=cli, args=())
	y.start()