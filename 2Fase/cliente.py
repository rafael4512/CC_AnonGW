import http.client
import threading
import sys
import time

def cli():
	BODY = ""
	conn = http.client.HTTPConnection("127.0.0.1", 80)
	a=conn.request("GET", "/file1", BODY)
	response = conn.getresponse()
	#print(type(a))
	#print(response)#, response.reason)
	aux=response.read(2000)
	#time.sleep(0.3)
	print("\nCliente1:",aux)#"Thread:ID->",threading.get_ident(),
	  

def cli2():
	BODY = "***filecontents***"

	conn = http.client.HTTPConnection("127.0.0.1", 80)
	conn.request("GET", "/", BODY)
	response = conn.getresponse()
	#print(response)#, response.reason
	print("\nCliente2",response.read(2000))
	  



for x in range(0,50):
	y=threading.Thread(target=cli, args=())
	y2=threading.Thread(target=cli2, args=())
	#if (x==3):
	#	print("sleep\n")
	#	time.sleep(0.3)
	#if (x==6):
	#	print("sleep\n")
	#	time.sleep(0.2)
	y.start()
	y2.start()
	#time.sleep(0.5)