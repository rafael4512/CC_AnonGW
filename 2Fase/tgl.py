#coding: utf-8 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


#classe para o cabeçalho dos pacotes do protocolo ANONGW
class Header:
	#Método construtor (306 bits de cabeçalho).A assinatura tem 256.
	def __init__(self,sig,isQuery,ultimoPac,id_cliente,n_ped,msg):
		self.sig=sig
		self.isQuery=isQuery
		self.ultimoPac=ultimoPac
		self.id_cliente=id_cliente
		self.n_ped=n_ped
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

	def converte(self):
		bits  = '{0:01b}'.format(self.isQuery)		#1 	 bit
		bits += '{0:01b}'.format(self.ultimoPac)	#1	 bit
		bits += '{0:016b}'.format(self.id_cliente)	#16	 bits
		bits += '{0:032b}'.format(self.n_ped)		#32  bits
		byts  = self.sig + bits.encode() + self.msg
		return byts
	
	def __str__(self):
		return "Header:\nSig:"+str(self.sig)+"\nQuery:"+str(self.isQuery)+"\nUltimoPacote:"+str(self.ultimoPac)+"\nId_Cliente:"+str(self.id_cliente)+"\nN_Ped:"+str(self.n_ped)+"\nDATA:"+str(self.msg)



def desconverte(byts):
	b=byts[256:306].decode()
	#print("Header:",b,"\n")
	#print("4444444\n")
	sig=byts[:256]
	#print("\tgetSignature::",sig)
	isQuery=int(b[0],2)
	#print("\tisQuery:",isQuery)
	ultimoPac=int(b[1],2) 
	#print("\tUltimoPAC:",ultimoPac)
	id_cliente=int(b[2:18],2)
	#print("\tId:",id_cliente)
	n_ped=int(b[18:50],2)
	#print("\tNped:",n_ped)
	msg=byts[306:]
	#print("\t",msg)
	return Header(sig,isQuery,ultimoPac,id_cliente,n_ped,msg)








