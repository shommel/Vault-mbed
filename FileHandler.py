from pyb import SDCard
from os import listdir, mkdir

def refreshSD():
	return SDCard()

def isSDPresent():
	'''
	bool value if sd card is present or not
	'''

	#refreshing sd card object 
	sd = refreshSD()
	return sd.present()

def read(path, mode='r'):
	'''
	reads file on flash or sd card and returns blob of data
	'''
	#refreshing sd card object if need be 
	if 'sd' in path.lower().split('/'):
		sd = refreshSD()

	fi = open(path, mode)
	data = fi.read()
	fi.close()

	return data


def write(path, data, mode='w'):
	'''
	writes to file on flash or sd card and returns number of bytes written
	'''
	#refreshing sd card object if need be
	if 'sd' in path.lower().split('/'):
		sd = refreshSD()

	fo = open(path, mode)
	res = fo.write(data)
	fo.close()

	return res

def initTxnDir():
	'''
	creates the transactions directory in board's flash if it doesn't already exist
	'''
	DIRECTORY_NAME = 'transactions'

	if DIRECTORY_NAME not in listdir('/flash'):
		mkdir('/flash/'+DIRECTORY_NAME)
		return 1

	return 0