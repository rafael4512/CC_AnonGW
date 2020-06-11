#coding: utf-8 

#classe para o cabeçalho dos pacotes do protocolo ANONGW
class Header:
	#Método construtor (306 bits de cabeçalho).A assinatura tem 256.
	def __init__(self,sig,isQuery,ultimoPac,id_cliente,n_ped,port,msg):
		self.sig=sig
		self.isQuery=isQuery
		self.ultimoPac=ultimoPac
		self.id_cliente=id_cliente
		self.n_ped=n_ped
		self.port=port#porta de onde veio o pedido
		self.msg=msg

	def getCliente(self):
		return self.id_cliente

	def getNumPed(self):
		return self.n_ped

	def getMsg(self):
		return self.msg
	
	def is_ultimoPac(self):
		return self.ultimoPac

	def getSignature(self):
		return self.sig

	def get_isQuery(self):
		return self.isQuery
	def getPort(self):
		return self.port

	def converte(self):
		bits  = '{0:01b}'.format(self.isQuery)		#1 	 bit
		bits += '{0:01b}'.format(self.ultimoPac)	#1	 bit
		bits += '{0:016b}'.format(self.id_cliente)	#16	 bits
		bits += '{0:032b}'.format(self.n_ped)		#32  bits
		bits += '{0:016b}'.format(self.port)
		byts  = self.sig + bits.encode() + self.msg
		return byts
	
	#def __str__(self):
	#	return "Header:\nSig:"+str(self.sig)+"\nQuery:"+str(self.isQuery)+"\nUltimoPacote:"+str(self.ultimoPac)+"\nId_Cliente:"+str(self.id_cliente)+"\nN_Ped:"+str(self.n_ped)+"\nDATA:"+str(self.msg)



def desconverte(byts):
	b=byts[256:322].decode()
	sig=byts[:256]
	isQuery=int(b[0],2)
	ultimoPac=int(b[1],2) 
	id_cliente=int(b[2:18],2)
	n_ped=int(b[18:50],2)
	port=int(b[50:66],2)
	msg=byts[322:]
	return Header(sig,isQuery,ultimoPac,id_cliente,n_ped,port,msg)








