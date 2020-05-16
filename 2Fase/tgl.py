#coding: utf-8 
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64



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



#gerador de chaves ->(private,public)
def generate_keys():
    modulus_length = 1024

    key = RSA.generate(modulus_length)
    #print (key.exportKey())

    pub_key = key.publickey()
    #print (pub_key.exportKey())

    return key, pub_key


#encripta uma msg com uma chave.Retorna a mensagem codificada e em byts.
def encrypt_private_key(a_message, private_key):
    encryptor = PKCS1_OAEP.new(private_key)
    encrypted_msg = encryptor.encrypt(a_message)
    #print(encrypted_msg)
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)
    #print(encoded_encrypted_msg)
    return encoded_encrypted_msg


# desencripta uma msg com uma chave.Retorna a msg desencriptada!
def decrypt_public_key(encoded_encrypted_msg, public_key):
    encryptor = PKCS1_OAEP.new(public_key)
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    #print(decoded_encrypted_msg)
    decoded_decrypted_msg = encryptor.decrypt(decoded_encrypted_msg)
    #print(decoded_decrypted_msg)
    return decoded_decrypted_msg




#Exemplo de funcionamento.
#def main():
#  private, public = generate_keys()
#  print (private)
#  message = b'Hello world'
#  encoded = encrypt_private_key(message, public)
#  msg=decrypt_public_key(encoded, private)
#  print (msg)






