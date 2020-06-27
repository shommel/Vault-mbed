from json import loads 
from bitcoin import script
from bitcoin import ec
from bitcoin.networks import NETWORKS
from ubinascii import unhexlify, hexlify
from bitcoin.transaction import Transaction, TransactionInput, TransactionOutput
from bitcoin import compact
from deletedkey import *
from FileHandler import *

pk = DeletedKey() #the deleted private key

def getTxid(tx):
    return hexlify(hashlib.sha256(tx.serialize()).digest())

def getAmount(tx):
    amount = 0
    for out in tx.vout:
        amount += out.value

    return amount

def PrepareVaultResponse(msg):
    '''
    Prepare Vault response
    will respond with the address of newly generated private key
    alogn with signature of 'signThis'
    '''
    signThis = msg 
    pk.generate()
    sig = hexlify(pk.sign(signThis).serialize())
    addr = script.p2pkh(pk.get_pubkey()).address()
    
    return [addr, sig]

def FinalizeVaultResponse(msg):
    '''
    Finalize Vault response
    reads the unsigned hex of the P2TST, signs and saves it. 
    then sends back the txid of the p2tst to computer

    '''
    unvault_tx = Transaction.parse(unhexlify(msg)) 
    h = unvault_tx.sighash_legacy(0, script.p2pkh(pk.get_pubkey()))
    sig = pk.sign(h)
    unvault_tx.vin[0].script_sig = script.script_sig_p2pkh(sig, pk.get_pubkey())

    pk.delete() # delete the private key
    isDeleted = pk.key == None
    txid = getTxid(unvault_tx)

    PATH = '/flash/transactions/' + str(txid)
    write(PATH, hexlify(unvault_tx.serialize())) #saving P2TST to storage on board
    
    return [isDeleted, txid]

def UnvaultResponse(msg):
    res = []
    for txid in msg:
        res.append(read('/flash/transactions/' + str(txid)))

    return res