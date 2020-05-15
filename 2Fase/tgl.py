#coding: utf-8 
from cryptography.fernet import Fernet


class Header:
	#Método construtor
	def __init__(self,isQuery,tam,id_cliente,n_ped,msg):
		self.isQuery=isQuery
		self.tam=tam
		self.id_cliente=id_cliente
		self.n_ped=n_ped
		self.msg=msg

	def getCliente(self):
		return self.id_cliente

	def getNumPed(self):
		return self.n_ped

	def getMsg(self):
		return self.msg

	
	def getTam(self):
		return self.tam

	def converte(self):
		bits = '{0:01b}'.format(self.isQuery)
		bits += '{0:016b}'.format(self.tam)
		bits += '{0:016b}'.format(self.id_cliente)
		bits += '{0:016b}'.format(self.n_ped)
		byts = bits.encode() +self.msg
		return byts

def desconverte(byts):
	b=byts.decode()
	isQuery=int(b[0],2)
	tam=int(b[1:17],2) 
	id_cliente=int(b[18:33],2)
	n_ped=int(b[34:49],2)
	msg=b[49:]
	return Header(isQuery,tam,id_cliente,n_ped,msg)
