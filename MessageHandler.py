'''
Message IDs: Corresponding Messages
0			: PrepareVault(signThis) - computer sends, board receives
1			: PrepareVaultResponse(Address, sig(signThis)) - board sends, computer receives
2			: FinalizeVault(unsigned P2TST)	- computer sends, board receives
3			: FinalizeVaultResponse(txid, isDeleted) - board sends, computer receives
4			: UnvaultRequest([txid_list]) - computer sends, board recieves
5			: UnvaultResponse([[p2tst_list]]) - board sends, computer receives
6			: GetDevicePublicKey() - computer sends, board recieves
7			: DevicePublicKey()	- board sends, computer receives
'''
#lightweight implementation of serial communication protocol 
from pyb import UART
from TransactionHandler import *
import time

CONSTANT	= '___' #divider between msg id and message
MSG_DIVIDER	= '##?' #divider between parts of the data
	
#setting up UART comms
uart = UART(3, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

def serializeField(data):
	if isinstance(data, bytes):
		return data
	elif isinstance(data, str):
		return bytes(data, 'utf8')
	elif (isinstance(data, int)) or (isinstance(data, bool)):
		return bytes([data])
	else:
		print('unrecgonized data type...')
		return False

def read_data():
	buffer = b''
	buffer += uart.read()
	print("Initial buffer:\t", buffer)
	while(buffer[-1] != b'$'[0]): # '$' will signify the end of total message
		print('message longer than 64 bytes. ')
		data = uart.read()
		if type(data) != type(None):
			print("adding to buffer")
			buffer += data
		time.sleep_ms(200)

	buffer = buffer[0:-1]
	print("Fully Received message:\t", buffer)
	unpack_data(buffer)

def send_data(buffer):
	uart.write(buffer)

def unpack_data(buffer):
	decoded_msg = buffer.decode('utf8').split(CONSTANT)
	msgId = int.from_bytes(bytes(decoded_msg[0], 'utf8'), 'big') #decode the msgId

	if(msgId == 0):
		PrepareVault_handler(decoded_msg[1])

	elif(msgId == 2):
		FinalizeVault_handler(decoded_msg[1])

	elif(msgId == 4):
		Unvault_handler(decoded_msg[1])
	else:
		print("unidentified msg id")
		return 1

def pack_data(msg, msgId):

	#preparing the message to send back to computer
	buffer = bytes([msgId]) + bytes(CONSTANT, 'utf8')

	#need to split up data to differentiate objects in message 
	for i in range(len(msg)):
		buffer += serializeField(msg[i])
		if i < (len(msg)-1):
			buffer += bytes(MSG_DIVIDER, 'utf8')
	send_data(buffer)

def PrepareVault_handler(msg):
	res = PrepareVaultResponse(msg)
	pack_data(res, 1)

def FinalizeVault_handler(msg):
	res = FinalizeVaultResponse(msg)
	print('here')
	pack_data(res, 3)

def Unvault_handler(msg):
	res = UnvaultResponse(msg)
	pack_data(res, 5)

