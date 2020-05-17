#coding: utf-8
#Teste->	  python3 AnonGW.py 127.0.0.1:81 6667 127.0.0.1:6666
import sys
import signal
import socket
import time
import tgl
import threading
from random import randint



HOST = sys.argv[1]		#endereco do host.
PORT_UDP=int(sys.argv[2]) 	# porta de Listen para anonGW
peer=[]				#Os outros anonGW's.
keySend=dict()
clientId=dict()
ServPORT=8000 #porta do servidor
Tam_PACK=102
Clientes=1	#acumaldor de Id's para clientes 

iid_lock = threading.Lock()# lock responsavel pelo  increment ID.

#Incrementa a Variavel Clientes.
def next_id():
    global Clientes
    with iid_lock:
        result = Clientes
        Clientes += 1
    return result

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
	data = conn.recv(4096) 			#Recebe o pedido.
	id = 1#gera um Id para o cliente.
	clientId[id_cli]=(conn,addr,0)
	#print("ID_CLIENTE:",id_cli,"\n")
	pacote=tgl.Header(1,len(data),id_cli,0,data)#sQuery,id_cliente,n_ped,msg)
	pacBin=pacote.converte()#pacote em Byts
	resp=enviarPedidoAGW(pacBin,peer[randint(0, (len(peer)-1))]) #envia o pedido a outro anonGW

	#print("XxXXXXXx",resp)
	#conn.sendto(resp,clientId[id_cli]) #envia  a resposta ao Cliente
	#conn.close()
	return True



#Metod usado pelo segundo anonGW,que envia a query ao servidor e renvia para anonGW
def receberPedidoAnon(UDPServerSocket,addr,data):
	pacote=tgl.desconverte(data)						#deconverte pq precisa de mandar apenas o pedido ao servidor .
	res = enviarServ(ServPORT,pacote.getMsg().encode()) #se já vier de um anonGW
	#print("len(msg):::::",len(res.decode()))
	divideEmPacotes(UDPServerSocket,addr,res,pacote.getCliente())
	#pacote=tgl.Header(0,len(res),1,0,res)				#cria um pacote
	#pacBin=pacote.converte()							#tranforma o pacote em Byts
	#UDPServerSocket.sendto(pacBin,addr)					#renvenvia a resposta ao anonGW 
	

#divide em pacotes e manda
def divideEmPacotes(UDPServerSocket,addr,msg,id_cli):
	tam=len(msg)
	#print("len(msg):::::",tam)
	n_ped=1
	while(len(msg) >= Tam_PACK):
		pacote=tgl.Header(0,tam,id_cli,n_ped,msg[:Tam_PACK])
		msg=msg[Tam_PACK:]
		pacBin=pacote.converte()
		n_ped+=1
		#print ("DATA",pacote.desconverte())
		UDPServerSocket.sendto(pacBin,addr)	#renvenvia a resposta ao anonGW 
	#envia o ultimo pacote.
	pacote=tgl.Header(0,tam,id_cli,n_ped,msg[:len(msg)])
	pacBin=pacote.converte()
	UDPServerSocket.sendto(pacBin,addr)	


#envia um Pedido ao servidor , e retorna a resposta. Tem de receber o pedido em byts(Não MEXER, está pronta!)
def enviarServ(port,pedido): 
	resp = bytearray()# array com os dados
	try:
		ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		ss.connect(('localhost', port))#socket para o servidor
		ss.sendall(pedido) # envia os dados para o serv 
		while True:
			dados = ss.recv(1024) #recebe 1024 bits 
			if not dados:
				break
			resp.extend(dados)
	except Exception as e: print(e)
	finally:
		ss.close() # fecha a conexao
	return resp 




def enviarPedidoAGW(msg,peer_addr):
	sp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket UDP
	sp.sendto(msg,(peer_addr[0], peer_addr[1]))#envia a 1 anowGw
	resp=bytearray()
	tam_acc=0# acumulador temporário de tamanho de cada pacotes.
	while True:
		(dados,adr) = sp.recvfrom(Tam_PACK+49) #recebe 1024 bits
		pacote=tgl.desconverte(dados)
		#print("Tam_PACK:",pacote.getTam(),"\n")
		#ver ordem!
		#print(pacote.getNumPed(),"\t",pacote.getCliente())
		(conn,addr,acc) = clientId[pacote.getCliente()]
		tam_acc= acc +len(dados)-49
		atualizaDic(pacote.getCliente(),(conn,addr,tam_acc))
		(c1,a1,acc2)=clientId[pacote.getCliente()]
		print("cliente:",pacote.getCliente(),len(dados)-49)
		conn.sendto(pacote.getMsg().encode(),addr)# envia a resposta para o cliente,do ultimo AnonGw.
		if (tam_acc==pacote.getTam() & tam_acc!=0):
			print("tam_acc:",tam_acc,"==",pacote.getTam(),"<-tam do pacotte")
			conn.close()
			break
		tam_acc=0
	return resp
 





def initTcpSocket():
	try:
		#signal.signal(signal.SIGINT, signal_handler)  #fechar o anonGW .
		s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket TCP
		h=parsePeer(HOST)
		s.bind((h[0],h[1]))
		s.listen(40) #Permite ter 40 pedidos antes de comecar a rejeitar.(Multicast)
		print('\tAnonGW Disponivel!')
		i=1# numero de pedidos recebidos
		while True:
			print("Waiting:",i)
			i+=1
			conn, addr = s.accept() # aceita uma coneção e cria um socket novo
			x = threading.Thread(target=receberPedidoCli, args=(conn,addr,next_id()))#thread para receber o pedido.
			x.start()
	except socket.error:
		print ("\n\tErro ao criar o socket TCP!")
	finally:
		s.close()







#Inicia o  anonGW
def init():
	x = threading.Thread(target=initTcpSocket, args=())
	x.start()
	h=parsePeer(HOST)
	UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	UDPServerSocket.bind((h[0], PORT_UDP))
	i=1
	while True:
		(data,addr) = UDPServerSocket.recvfrom(4096)
		print("ped:",i,"\t",UDPServerSocket.getsockname(),addr)
		i+=1
		#if (addr[1]!=PORT_UDP):
		y=threading.Thread(target=receberPedidoAnon, args=(UDPServerSocket,addr,data))
		y.start()
		#UDPServerSocket.sendto(bytesToSend, address)

init()




