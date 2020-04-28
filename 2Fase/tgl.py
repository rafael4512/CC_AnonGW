#coding: utf-8
from cryptography.fernet import Fernet


class Header:
	#Método construtor
	def __init__(self,isQuery,id_cliente,n_ped,msg):
		self.isQuery=isQuery
		self.id_cliente=id_cliente
		self.n_ped=n_ped
		self.msg=msg


