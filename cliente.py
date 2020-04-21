import socket
import threading
def cli():
	l = threading.Lock()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	l.acquire() 	
	s.connect(('localhost', 80))
	s.send("GET / HTTP/1.1\r\nHost: 0.0.0.0\r\nUser-Agent: curl/7.64.1\r\nAccept: */*\r\n\r\n")
	while True:
		data=s.recv(1024)
		if not data:
			l.release()
			break;
		print data



for x in range(0,20):
	x = threading.Thread(target=cli, args=())#
	x.start()