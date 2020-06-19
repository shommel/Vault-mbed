from bitcoin import script
from bitcoin import ec
from bitcoin.networks import NETWORKS
from ubinascii import unhexlify, hexlify
from bitcoin.transaction import Transaction, TransactionInput, TransactionOutput
from bitcoin import compact
from deletedkey import *
from FileHandler import *

pk = DeletedKey() #the deleted private key

def PrepareVault():
    '''
    Prepare Vault response
    will respond with the address of newly generated private key
    alogn with signature of 'signThis'
    '''
    #data = sd_read(PATH_TO_FILE)
    #signThis = data.signThis
    signThis = 'hello world' #just having a test value 
    pk.generate()
    sig = hexlify(pk.sign(signThis).serialize())
    addr = script.p2pkh(pk.get_pubkey()).address()

    #write(PATh_TO_FILE, [addr, sig])
    return [addr, sig, hexlify(pk.get_pubkey().serialize())]

def FinalizeVault():
    '''
    Finalize Vault response
    reads the unsigned hex of the P2TST from the SD Card

    '''
    #data = sd_read(PATH_TO_FILE)
    # unvault_tx = Transaction.parse(unhexlify(data.txn)) 
    # h = unvault_tx.sighash_legacy(0, script.p2pkh(pk.get_pubkey()))
    # sig = pk.sign(h)
    # unvault_tx.vin[i].script_sig = script.script_sig_p2pkh(sig, pk.get_pubkey())

    # pk.delete() # delete the private key
    # isDeleted = pk.key == None
    # #save_to_filesystem(hexlify(unvault_tx.serialize()))) #saving P2TST to storage on board
    
    # #writing if key is deleted and the txid of P2TST
    # #write(PATH, [isDeleted, hexlify(unvault_tx.txid())]
    # return [isDeleted, hexlify(unvault_tx.txid())]
    return 0

def Unvault():
    return 0