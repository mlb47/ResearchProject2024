from cryptography.hazmat.primitives.asymmetric import rsa, padding, utils
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, AESCCM, ChaCha20Poly1305
from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES, CAST5
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
import os
import base64

def RSAencrypt(message, pem):
    public_key = load_pem_public_key(pem, backend=default_backend())
    ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        )
    )
    encodedtext = base64.b64encode(ciphertext)  
    return encodedtext

def ECBencrypt(message, key):
    encryptor = Cipher(
        algorithms.AES(key),
        modes.ECB(),
        backend=default_backend()
        ).encryptor()
    ciphertext = encryptor.update(message)
    encodedtext = base64.b64encode(ciphertext)  
    return encodedtext

def generateIV():
    iv = os.urandom(8)
    return iv

def TripleDESencrypt(message, key ,iv):
    encryptor = Cipher(
        algorithms.TripleDES(key),
        modes.CBC(iv),
        backend=default_backend()
        ).encryptor()
    ciphertext = encryptor.update(message)
    encodedtext = base64.b64encode(ciphertext)
    return encodedtext

def CAST5encrypt(message, key ,iv):
    encryptor = Cipher(
        algorithms.CAST5(key),
        modes.CBC(iv),
        backend=default_backend()
        ).encryptor()
    ciphertext = encryptor.update(message)
    encodedtext = base64.b64encode(ciphertext)
    return encodedtext

def generateNonce():
    nonce = os.urandom(12)
    return nonce

def GCMencrypt(message, key, nonce):
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, message, None)
    encodedtext = base64.b64encode(ciphertext)  
    return encodedtext

def CCMencrypt(message, key, nonce):
    aesccm = AESCCM(key)
    ciphertext = aesccm.encrypt(nonce, message, None)
    encodedtext = base64.b64encode(ciphertext)  
    return encodedtext

def Chaencrypt(message, key, nonce):
    chacha = ChaCha20Poly1305(key)
    ciphertext = chacha.encrypt(nonce, message, None)
    encodedtext = base64.b64encode(ciphertext)  
    return encodedtext

def AESencrypt_withECCkey(message, ecc_key):
    aesgcm = AESGCM(ecc_key)
    ciphertext = aesgcm.encrypt(nonce, message, None)
    encodedtext = base64.b64encode(ciphertext)  
    return encodedtext