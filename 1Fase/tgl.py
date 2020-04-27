#coding: utf-8
from cryptography.fernet import Fernet


class HeaderP:
	#Método construtor
	def __init__(self,id_cliente,msg):
		self.id_cliente=id_cliente
		self.msg=msg


class HeaderR:
	#Método construtor
	def __init__(self,id_cliente,n_ped,msg):
		self.id_cliente=id_cliente
		self.n_ped=n_ped
		self.msg=msg




