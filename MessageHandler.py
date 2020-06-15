from pyb import LED
from messages_upb2 import *
from messagesBitcoin_upb2 import *
from messagesCommon_upb2 import *
from messagesManagement_upb2 import *

class MessageHandler():
	'''
	This class will act as a Protobuf message interface between the Computer Interface and dev board.

	The board will be implementing the same Protobuf protocol as described in Trezorlib found below.
	https://github.com/trezor/trezor-common/blob/master/protob/protocol.md
	'''

	def __init__(self, uart, msgType = 0, msgSize = 0, remainder = 0, msg=''):
		self.uart		= uart			#serial communications
		self.msgType 	= msgType 		#type of message
		self.msgSize 	= msgSize		#size of message
		self.remainder 	= remainder 	#remainder of message left to be read
		self.msg 		= msg 			#the actual message (excluding headers)
		
	def read_data(self):
		result = self.unpack_data(self.uart.read(64))
		return result

	def send_data(self, buffer):
		return self.uart.write(buffer)

	def unpack_data(self, buffer):
		if(buffer[0:3] == b'?##'): #the buffer contains the first message
			#stripping out necessary fields from header
			self.msgType = int( str(buffer[3]) + str(buffer[4]) ) 
			self.msgSize = int( str(buffer[5]) + str(buffer[6]) + str(buffer[7]) + str(buffer[8]) )
			
			#no point continuing with reading if the size of message is initially 0
			if(self.msgSize != 0):
				#reading the remainder of first packet, and determining if we need to continue reading next packet
				self.msg = buffer[9: 9 + min(self.msgSize, 55)]
				self.remainder = self.msgSize - min(self.msgSize, 55)

			else:
				self.remainder = 0 #reset the remainder if there is no message to read

		elif( (buffer[0] == b'?') and (buffer[1] != b'#') ): #the buffer contains a subsequent message
			self.msg += buffer[1: min(self.msgSize, 63)]
			self.remainder -= min(self.msgSize, 63)

		else:
			print('Message recieved has invalid header constants.')
			return -1

		if(self.remainder == 0): #full message recieved
			#message types can be found in messages_upb2.py
			if(self.msgType == 55): 
				LED(1).toggle()
				self.get_features_handler()

			else:
				LED(4).toggle()
				print('Message recieved has invalid message type. Refer to list of message types found in messages_upb2.py')

			return 0 #message fully read, stop bugging computer

		return 1 #message not fully read, keep bugging computer

	def pack_data(self):

		#preparing the first message
		buffer = b'?##'
		buffer += (self.msgType).to_bytes(2, 'big')
		buffer += (self.msgSize).to_bytes(4, 'big')
		buffer += self.msg[0 : min(self.msgSize, 55)]

		#need to pad string with zeroes if need be
		if(self.msgSize < 55): 
			buffer += b'0' * (55 - self.msgSize)

		self.remainder -= min(self.msgSize, 55)
		self.send_data(buffer)
		#print("Sending: ", buffer)

		#more messages to be sent
		while(self.remainder > 0):

			#preparing subsequent message(s)
			buffer = b'?'
			index = self.msgSize - self.remainder 
			buffer += self.msg[index : index + min(self.remainder, 63)]

			#need to pad string with zeroes if need be
			if(self.remainder < 63): 
				buffer += b'0' * (63 - self.remainder)

			self.remainder -= min(self.remainder, 63)
			self.send_data(buffer)
			#print("Sending: ", buffer)


	#Message Handler functions 
	def get_features_handler(self):
		res = FeaturesMessage()

		#filling up Features Message response with bogus information
		res.vendor = "0483"
		res.major_version = 0
		res.minor_version = 0
		res.patch_version = 0
		res.bootloader = 0
		res.device_id= '374b'
		res.pin_protection = 0
		res.passphrase_protection = 0
		res.language = "ENG"
		res.label = "STM"
		res.initalized = 1
				# res.revision				= b'0'
				# res.bootloader_hash			= b'0'
		res.imported = 0
		res.pin_cached = 0
		res.passphrase_cached = 0
		res.firmware_present = 1
		res.needs_backup = 0
		res.flags = 0
		res.model = "STM32F469NI-DISCOVERY"
		res.fw_major = 0
		res.fw_minor = 0
		res.fw_patch = 0
		res.fw_vendor = "0483"
		#res.fw_vendor_keys = b'0'
		res.unfinished_backup = 0
		res.no_backup = 0
		# res.recovery_mode = 0
		# res.sd_card_present = 0
		# res.sd_protection = 0
		# res.wipe_code_protection = 0

		#preparing the header for the response message
		self.msg 		= res.serialize()
		self.msgType 	= 17 #message type for Features message
		self.msgSize 	= len(res.serialize())
		self.remainder 	= len(res.serialize())

		self.pack_data()

