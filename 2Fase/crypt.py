# RSA helper class for pycrypto
# Copyright (c) Dennis Lee
# Date 21 Mar 2017

# Description:
# Python helper class to perform RSA encryption, decryption, 
# signing, verifying signatures & keys generation

# Dependencies Packages:
# pycrypto 

# Documentation:
# https://www.dlitz.net/software/pycrypto/api/2.6/



#BEGIN-____-



from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import rsa

hash = "SHA-256"

def newkeys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private

def importKey(externKey):
    return RSA.importKey(externKey)

def getpublickey(priv_key):
    return priv_key.publickey()

def encrypt(message, pub_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def sign(message, priv_key, hashAlg="SHA-256"):
    global hash
    hash = hashAlg
    signer = PKCS1_v1_5.new(priv_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)

def main():
    msg1 = b"Hello Tony, I am Jarvis!"
    msg2 = b"Hello Toni, I am Jarvis!"

    keysize = 2048

    (public, private) = rsa.newkeys(keysize)

    # https://docs.python.org/3/library/base64.html
    # encodes the bytes-like object s
    # returns bytes
    encrypted = b64encode(rsa.encrypt(msg1,public))                 #encripta com chave publica
    # decodes the Base64 encoded bytes-like object or ASCII string s
    # returns the decoded bytes
    signature = b64encode(rsa.sign(msg1, private, "SHA-512"))       #assina com a privada
    decrypted = rsa.decrypt(b64decode(encrypted),private)           #desencripta com a privada 
    verify = rsa.verify(msg1, b64decode(signature), public)         #verifica

    #print(private.exportKey('PEM'))
    #print(public.exportKey('PEM'))
    print("Encrypted: " + encrypted.decode('ascii'))
    print("Decrypted: '%s'" % (decrypted))
    print("Signature: " + signature.decode('ascii'))
    print("Verify: %s" % verify)
    #rsa.verify(msg2, b64decode(signature), public)

if __name__== "__main__":
    main()







#END -FIRST PROGRAM






