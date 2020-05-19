from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import sys
from types import ModuleType, FunctionType
from gc import get_referents
import cryptography.exceptions

#Gera e armazena um par de Chaves(Pública e Privada)
def generate_key(name): 
    private_key = rsa.generate_private_key( #Cria Chave Privada
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
    public_key = private_key.public_key() #Cria Chave Pública

    pem = private_key.private_bytes( #Serializa Chave Privada
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    x = name + '_private_key.pem'
    with open(x, 'wb') as f: #Guarda Chave Privada
        f.write(pem)

    pem = public_key.public_bytes( #Serializa Chave Pública
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    y = name + '_public_key.pem' 
    with open(y, 'wb') as f: #Guarda Chave Pública
        f.write(pem)

#assina uma mensagem, passando o nome do ficheiro(colocado anteriormente na funcão generate_key).Retorna a assinatura
def signing(name,message):
    x = name + '_private_key.pem'
    with open(x, "rb") as key_file: #Lê a Chave Privada
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    y = name + '_public_key.pem'
    with open(y, "rb") as key_file: #Lê a Chave Pública
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    signature = private_key.sign( #Assina Mensagem
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature #Retorna Assinatura

#assina uma mensagem, passando o nome do ficheiro(colocado anteriormente na funcão generate_key), a assinatura e a mensagem.Retorna um excecao se a assinatura nao for correta.
def verification(name,signature,message):
    x = name + '_private_key.pem'
    with open(x, "rb") as key_file: #Lê a Chave Privada
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
           )
    y = name + '_public_key.pem'
    with open(y, "rb") as key_file: #Lê a Chave Pública
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    public_key.verify( #Verifica a Mensagem
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

#encripta uma msg
def encrypt(message,name_publicKey):
    y = name_publicKey + '_public_key.pem'
    with open(y, "rb") as key_file: #Lê a Chave Pública
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
    )

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

#desencripta uma msg
def decrypt(ciphertext,name_privateKey):
    x = name_privateKey + '_private_key.pem'
    with open(x, "rb") as key_file: #Lê a Chave Privada
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
    )

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext





#EXEMPLO DE FUNCIONAMENTO:
#generate_key("6666")
#message = "Ola sou o José!" 
#ciphertext=encrypt(message.encode(),"6666") 
#s=signing('6666',ciphertext)
#print(s)
#msg=decrypt(ciphertext,"6666") 
#try:
#    verification('6666',s,ciphertext)#receve o texto cifrado e verifica se a msg tem essa signatura.
#    print("VERIFICADO COM SUCESSO")
#    print ("\ntexto",msg.decode())
#except cryptography.exceptions.InvalidSignature:
#    print("Cliente desconhecido")





#key = Fernet.generate_key()
#print("Chave original \t",key)
#ciphertext=encrypt(key,"6666")
#s=signing('6666',ciphertext)
#try:
#    verification('6666',s,ciphertext)#receve o texto cifrado e verifica se a msg tem essa signatura.
#    print("VERIFICADO COM SUCESSO")
#except cryptography.exceptions.InvalidSignature:
#    print("Cliente desconhecido")
#
#msg=decrypt(ciphertext,"6666") 
#print("\n\n FINAl:",msg)
#plain=f.decrypt(token)


