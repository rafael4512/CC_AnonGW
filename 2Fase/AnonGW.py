#coding: utf-8
#Teste->	  python3 AnonGW.py 127.0.0.1:81 6667 127.0.0.1:6666
import sys
import signal
import socket
import time
import tgl
import threading
import crypt
from random import randint



HOST = sys.argv[1]		#endereco do host.
PORT_UDP=int(sys.argv[2]) 	# porta de Listen para anonGW
peer=[]				#Os outros anonGW's.
clientId=dict()
ServPORT=8000 #porta do servidor
Tam_PACK=1024
Clientes=1	#acumaldor de Id's para clientes 
iid_lock = threading.Lock()# lock responsavel pelo  increment ID.


#Incrementa a Variavel Clientes.
def next_id():
    global Clientes
    with iid_lock:
        result = Clientes
        Clientes += 1
    return result

#atualiza o dicionario dos clientes
def atualizaDic(id_cli,novoValue):
    global clientId
    with iid_lock:
         clientId[id_cli]=novoValue
    return True


#processa uma string necessaria para se conectar a outro anonGW.Devolve o par para se connectar diretamente ao socket
def parsePeer(str):
	l=str.split(":")#separa a string pelo char :, e coloca numa lista.
	if (len(l)==2):
		return (l[0],int(l[1]))
	else:
		return("-1",-1)


#coloca os anonGW conhecidos na lista de Peers.
for x in range(3, len(sys.argv)):
	aux =parsePeer(sys.argv[x])
	if (aux!=("-1",-1)):
         peer.append(aux)



#Função responsável por fechar o AnonGW,quando se envia SIGINT.
def signal_handler(sig, frame):
    print('\n\tAnonGW Fechado!')
    sys.exit(0)



#s->socket na porta 80
#conn ->socket para o cliente. VEr se precisamos do addr!!!!
def receberPedidoCli(conn,addr,id_cli):
	data = conn.recv(4096) 										 #Recebe o pedido.
	clientId[id_cli]=(conn,addr,0)								 #guarda a coneção no dicionario
	pacote=tgl.Header(1,0,id_cli,0,data)						 #encapsula num  pacote.
	pacBin_plain=pacote.converte()							     #pacote em Byts
	
	anon=peer[randint(0, (len(peer)-1))]						 #calcula o proximo anonGW 
	pacBin_cipher=crypt.encrypt(pacBin_plain,str(anon[1]))		 #encripta o pacote bin!
	#signing(str(PORT_UDP),pacBin_cipher)						 #asssina o pacote
	#print("\nPedido:"pacBin_cipher)
	resp=enviarPedidoAGW(pacBin_cipher,anon) 					 #envia o pedido a outro anonGW
	return True



#Metod usado pelo segundo anonGW,que envia a query ao servidor e renvia para anonGW
def receberPedidoAnon(UDPServerSocket,addr,data_cipher):
	#print("\nPedido encriptado:",data_cipher)								#mostrar o pedido encriptado!
	data=crypt.decrypt(data_cipher,str(UDPServerSocket.getsockname()[1]))	#desencripta a msg
	#print("\nPedido desencriptado:",data)									#mostrar o pedido desencriptado!
	pacote=tgl.desconverte(data)											#deconverte pq precisa de mandar apenas o pedido ao servidor .
	res = enviarServ(ServPORT,pacote,UDPServerSocket,addr)					#se já vier de um anonGW


#envia um Pedido ao servidor , e retorna a resposta. Tem de receber o pedido em byts(Não MEXER, está pronta!)
def enviarServ(port,pacote,UDPServerSocket,addr): 
	n_ped=1
	h=parsePeer(HOST)
	try:
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#socket TCP
		ss.connect((h[0], port))								#socket para o servidor
		ss.sendall(pacote.getMsg().encode()) 					#envia os dados para o serv 
		while True:
			dados = ss.recv(Tam_PACK) 							#recebe 1024 bits
			if not dados:
				pacote2=tgl.Header(0,1,pacote.getCliente(),n_ped,dados)		#encapsula os dados num pacote
				pacBin2=pacote2.converte()									#converte o pacote para binario
				UDPServerSocket.sendto(pacBin2,addr)						#envia o ultimo pacote para o anonGW
				break
			pacote=tgl.Header(0,0,pacote.getCliente(),n_ped,dados)			#encapsula os dados num pacote
			pacBin=pacote.converte()										#converte o pacote para binario
			n_ped+=1														#atualiza o numero do pacote.
			UDPServerSocket.sendto(pacBin,addr)								#envia a reposta do servidor para o anonGW 
	except Exception as e: 
		print(e)
		#print("OLA\n")
	finally:
		ss.close() # fecha a conexao




def enviarPedidoAGW(msg,peer_addr):
	sp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 	#socket UDP
	sp.sendto(msg,(peer_addr[0], peer_addr[1]))				#envia a 1 anowGw
	#tam_acc=0												# acumulador temporário de tamanho de cada pacotes.

	while True:
		(dados,adr) = sp.recvfrom(Tam_PACK+49) 			#recebe TamPAck bits + o cabeçalho. 
		pacote=tgl.desconverte(dados)
		(conn,addr,acc) = clientId[pacote.getCliente()]						#transforma os bits em um Objeto.
		if(pacote.getTam()==1 and len(pacote.getMsg())== 0):
			conn.close()
			break
		print("Cliente:",pacote.getCliente(),"\tN_Ped:",pacote.getNumPed(),"\n")
		#tam_acc= acc +len(dados)-49
		#atualizaDic(pacote.getCliente(),(conn,addr,tam_acc)) 
		#(c1,a1,acc2)=clientId[pacote.getCliente()]
		conn.sendto(pacote.getMsg().encode(),addr)# envia a resposta para o cliente,do ultimo AnonGw.
		#tam_acc=0
	sp.close()
	return True
 




#Inicia o uma thread para processar pedidos TCP de clientes.
def initTcpSocket():
	try:
		#signal.signal(signal.SIGINT, signal_handler)  			#fechar o anonGW .
		s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) 	#socket TCP
		h=parsePeer(HOST)										#separa a string, (ip_socket,porta)
		s.bind((h[0],h[1]))										#associa o socket ao endereco respectivo
		s.listen(40) 											#Permite ter 40 pedidos antes de comecar a rejeitar.(Multicast)
		print('\tAnonGW Disponivel!')
		while True:
			conn, addr = s.accept() # aceita uma coneção e cria um socket novo
			x = threading.Thread(target=receberPedidoCli, args=(conn,addr,next_id()))#thread para receber o pedido.
			x.start()
	except socket.error:
		print ("\n\tErro ao criar o socket TCP!")
	finally:
		s.close()




#Inicia o  anonGW
def init():
	try:
		geraChaves(PORT_UDP)#gera chaves privadas e publicas com o nome da porta UDP
		#signal.signal(signal.SIGINT, signal_handler)
		x = threading.Thread(target=initTcpSocket, args=())							  #thread reponsavel pela porta 80,atende pedidos TCP.
		x.start()																	  #inicia  thread reponsavel pela porta 80.
		h=parsePeer(HOST)															  #parse dos endereços.
		UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)#Socket UDP
		UDPServerSocket.bind((h[0], PORT_UDP))										  #associa o endereco ao socket
		
		i=1	#numero de threds
		while True:
			(data,addr) = UDPServerSocket.recvfrom(4096)
			#print("ped:",i,"\t",UDPServerSocket.getsockname(),addr)
			i+=1
			y=threading.Thread(target=receberPedidoAnon, args=(UDPServerSocket,addr,data))
			y.start()
	except Exception as e :
		print(e)
	finally:
		#x.join()
		UDPServerSocket.close()






def geraChaves(port):	
	crypt.generate_key(str(port))#funcao que gera as chaves

init()




