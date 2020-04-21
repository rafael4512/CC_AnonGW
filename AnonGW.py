#coding: utf-8
#Teste->	anonGW target-server 10.3.3.1 port 80 overlay-peers 10.1.1.2 10.4.4.2 10.4.4.3
import sys
import signal
import socket
import time
import threading
import thread


HOST = ''				
PORT=int(sys.argv[2]) 	# porta de Listen
peers=[]				#Os outros anonGW's.
for x in range(0, len(sys.argv)):
    peers.append(sys.argv[x]) 

ServPORT=8000 #porta do servidor
#s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Função responsável por fechar o AnonGW,quando se envia SIGINT.
def signal_handler(sig, frame):
    print('\n\tAnonGW Fechado!')
    sys.exit(0)




#s->socket na porta 80
#conn ->socket para o cliente
def receberPedido(conn):

	data = conn.recv(1024) # guarda o pedido do cliente em data 	
	res = enviarServ(ServPORT,data)	#envia o pedido para o servidor
	#fh=res.find("\r\n\r\n")#calcula a posição do fim do cabeçalho.
	#conn.sendall(res[fh+4:])	
	conn.sendall(res)	
	#print  "Enviado  com SUCESSO"
	#time.sleep(4)
	#e = threading.Event()
	#e.wait(10)
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
			print i
			i+=1
			conn, addr = s.accept() # aceita uma coneção e cria um socket novo
			x = threading.Thread(target=receberPedido, args=(conn,))#thred para receber o pedido.
			x.start()
			#thread.start_new_thread( receberPedido,(conn,))
			#receberPedido(conn)
	except socket.error:
		print "\n\tErro ao criar o socket-80"
	finally:
		s.close()



init()





#	Obter os parametros recebidos
# tarServ=sys.argv[1] 	#destino da mensagem. 
# HOST = ''				# Symbolic name meaning all available interfaces.
#PORT=int(sys.argv[2]) 		#Porta  em que o anonGW está a escuta.
 


