#coding: utf-8
#Teste Exemplo -> anonGW 0.0.0.0 80  10.1.1.2 10.4.4.2 10.4.4.3
import sys
import signal
import socket
import time
import threading
import thread

#Variaveis Globais
PORT=int(sys.argv[2]) 								 # porta de Listen
peers=[]											 #Os outros anonGW's.
for x in range(0, len(sys.argv)):
    peers.append(sys.argv[x]) 						 #peer's
ServPORT=8000 										 #porta do servidor
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket TCP listen


#Função responsável por fechar o AnonGW,quando se envia SIGINT.
def signal_handler(sig, frame):
    print('\n\tAnonGW Fechado!')
    s.close()
    sys.exit(0) 


#Recebe um pedido de um cliente.
def receberPedido(conn): 
	data = conn.recv(4096) # guarda o pedido do cliente em data 	
	if not data:
		conn.close()
	res = enviarServ(ServPORT,data)	#envia o pedido para o servidor
	conn.sendall(res)	
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
				ss.close()
				break
			resp.extend(dados) #coloca os byts no array.
	except Exception as e: print(e)
	finally:
		ss.close() # fecha a conexao
	return resp 



#Inicia o  anonGW
def init():
	try:
		signal.signal(signal.SIGINT, signal_handler)  #handler para fechar o anonGW com CRL-C.
		s.bind(('', PORT))#liga o socket à porta
		s.listen(10) #Permite ter 10 pedidos à espera,antes de comecar a rejeitar.(Multicast) 
		print('\tAnonGW Disponivel!')
		i=1
		while True:
			conn, addr = s.accept() # aceita uma coneção e cria um socket novo
			print i
			i+=1
			x = threading.Thread(target=receberPedido, args=(conn,))#thred para receber o pedido.
			x.start()
	except socket.error:
		print "\n\tErro ao criar o socket!Esperar que seja fechado"
	finally:
		s.close()


init()

