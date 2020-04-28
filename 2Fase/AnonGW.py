#coding: utf-8
#Teste->	anonGW target-server 10.3.3.1 port 80 overlay-peers 10.1.1.2 10.4.4.2 10.4.4.3
import sys
import signal
import socket
import time
import threading
import thread
from cryptography.fernet import Fernet


HOST = ''				
PORT=int(sys.argv[2]) 	# porta de Listen
peers=[]				#Os outros anonGW's.
keySend=dict()
clientId=dict()
for x in range(0, len(sys.argv)):
    keySend[sys.argv[x]]=Fernet.generate_key()
    #peers.append(sys.argv[x]) 

ServPORT=8000 #porta do servidor
#s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Função responsável por fechar o AnonGW,quando se envia SIGINT.
def signal_handler(sig, frame):
    print('\n\tAnonGW Fechado!')
    sys.exit(0)

def encrypt(msg,key):
	f = Fernet(key)
	return f.encrypt(msg)

def decrypt(msg,key):
	f=Fernet(key)
	return f.decrypt(m)






#s->socket na porta 80
#conn ->socket para o cliente
def receberPedido(conn,addr):
	
	data = conn.recv(4096) # guarda o pedido do cliente em data
	enviarPedidoAGW(data,"0.0.0.0",81) 
	conn.close()
	return res


#envia um Pedido ao servidor , e retorna a resposta.
def enviarServ(port,pedido): 
	resp = bytearray()# array com os dados
	try:
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.connect(('localhost', port))#socket para o servidor
		ss.sendall(pedido) # envia os dados para o serv
		i=1
		while True:
			dados = ss.recv(4092) #recebe 1024 bits
			if not dados:
				break
			resp.extend(dados) #coloca os byts no array.
	except Exception as e: print(e)
	finally:
		ss.close() # fecha a conexao
	return resp 

def enviarPedidoAGW(msg,peer,port):
	sp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket UDP
	anon_addr = (peer,port)
	sp.connect(anon_addr)
	m=encrypt(msg,keySend[peer])
	sp.sendto(keySend[peer],anon_addr)
	sp.sendto(m,anon_addr)

	return sp


#def receberPedidoAGW()
	

#Inicia o  anonGW
def init():

	try:
		signal.signal(signal.SIGINT, signal_handler)  #fechar o anonGW .
		s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		s.bind(('', PORT))
		s.listen(1) #Permite ter 40 pedidos antes de comecar a rejeitar.(Multicast)
		print('\tAnonGW Disponivel!')
		i=1
		while True:
			print("Waiting:",i)
			i+=1
			conn, addr = s.accept() # aceita uma coneção e cria um socket novo
			print addr
			x = threading.Thread(target=receberPedido, args=(conn,addr,))#thred para receber o pedido.
			x.start()
			#thread.start_new_thread( receberPedido,(conn,))
			#receberPedido(conn)
	except socket.error:
		print "\n\tErro ao criar o socket-80"
	finally:
		s.close()



init()






#Envia um pedido para um anonGW





#	Obter os parametros recebidos
# tarServ=sys.argv[1] 	#destino da mensagem. 
# HOST = ''				# Symbolic name meaning all available interfaces.
#PORT=int(sys.argv[2]) 		#Porta  em que o anonGW está a escuta.
 


