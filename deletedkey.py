from gc import collect
from bitcoin import ec
from ubinascii import hexlify, unhexlify
import hashlib
from pyb import ADC
from os import urandom
from random import choice

ADC_ops = ["A0", "A1", "A2", "A3", "A4", "A5", "A6"]

class DeletedKey:
	'''
	acting as an interface for the PrivateKey class in ec.py. 
	'''
	def __init__(self, key=None):
		self.key = key

	def generate(self):
		'''
		generating entropy and initializing private key 
		entropy both from RNG chip and analog-to-digital converters on board
		'''
		entropy = urandom(32) + b'dfahdsfjhsadkfjhsdljkhmndfb'
		ADC_entropy = bytes([ADC(choice(ADC_ops)).read() % 256 for i in range(2048)])
		self.key = ec.PrivateKey.parse(hashlib.sha256(entropy + ADC_entropy).digest())
		del entropy
		del ADC_entropy
		collect()

	def delete(self):
		'''
		a prototype of secure key deletion 
		'''
		del self.key
		self.key = None
		collect()
		return self.key == None 

	def sign(self, msg):
		'''
		sign an arbitrary message with the soon to be deleted private key
		this will be also be used to sign a tx
		
		return a signature object 
		'''
		if(len(msg) != 32): #a message of arbitrary length (i.e not part of a transaction)
			return self.key.sign(hashlib.sha256(msg).digest())

		return self.key.sign(msg)

	def get_pubkey(self):
		'''
		return the public key of the generated key 
		'''
		return self.key.get_public_key()

	def isDeleted(self):
		'''
		bool if private key is deleted
		'''
		return self.key == None