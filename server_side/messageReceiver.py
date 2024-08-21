#!/usr/bin/env python3
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, AESCCM, ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
import os
import base64
    
def RSAgeneratePrivateKey():
    private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
    )
    return private_key

def RSAserializePublicKey(private_key):
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    pem.splitlines()[0]
    b'-----BEGIN PUBLIC KEY-----'
    return pem

def RSAdecrypt(message, private_key):
    decoded = base64.b64decode(message)
    plaintext = private_key.decrypt(
    decoded,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    return plaintext
    
def ECBgenerateKey():
	key = os.urandom(32)
	return key
	
def ECBdecrypt(message, key):
	decoded = base64.b64decode(message)
	decryptor = Cipher(
		algorithms.AES(key), 
		modes.ECB(),
		backend=default_backend()
	).decryptor()
	plaintext = decryptor.update(decoded) + decryptor.finalize()
	return plaintext
	
def TripleDESgenerateKey():
	key = os.urandom(24)
	return key

def TripleDESdecrypt(message, key, iv):
	decoded = base64.b64decode(message)
	decryptor = Cipher(
		algorithms.TripleDES(key), 
		modes.CBC(iv),
		backend=default_backend()
	).decryptor()
	plaintext = decryptor.update(decoded)
	return plaintext

def CAST5generateKey():
	key = os.urandom(16)
	return key

def CAST5decrypt(message, key, iv):
	decoded = base64.b64decode(message)                                     
	decryptor = Cipher(
		algorithms.CAST5(key) , 
		modes.CBC(iv),
		backend=default_backend()
	).decryptor()
	plaintext = decryptor.update(decoded)
	return plaintext
			
		
def GCMgenerateKey():
	key = AESGCM.generate_key(bit_length=128)
	return key	
	
def GCMdecrypt(message, key, nonce):
	decoded = base64.b64decode(message)
	aesgcm = AESGCM(key)
	plaintext = aesgcm.decrypt(nonce, decoded, None)
	return plaintext
	
def CCMgenerateKey():
	key = AESCCM.generate_key(bit_length=128)
	return key	
	
def CCMdecrypt(message, key, nonce):
	decoded = base64.b64decode(message)
	aesccm = AESCCM(key)
	plaintext = aesccm.decrypt(nonce, decoded, None)
	return plaintext

def ChagenerateKey():
	key = ChaCha20Poly1305.generate_key()
	return key

def Chadecrypt(message, key, nonce):
	decoded = base64.b64decode(message)
	chacha = ChaCha20Poly1305(key)
	plaintext = chacha.decrypt(nonce, decoded, None)
	return plaintext
