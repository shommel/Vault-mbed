from bitcoin import script
from bitcoin import ec
from bitcoin.networks import NETWORKS
from ubinascii import unhexlify, hexlify
from bitcoin.transaction import Transaction, TransactionInput, TransactionOutput
from bitcoin import compact
from deletedkey import *
from FileHandler import *
import json 

pk = DeletedKey() #the deleted private key

def getTxid(tx):
    return hexlify(hashlib.sha256(tx.serialize()).digest())

def getAmount(tx):
    amount = 0
    for out in tx.vout:
        amount += out.value

    return amount
def PrepareVault():
    '''
    Prepare Vault response
    will respond with the address of newly generated private key
    alogn with signature of 'signThis'
    '''
    #data = json.loads(read('/sd/PrepareVault.json'))
    #signThis = data['signThis']
    signThis = 'hello world' #just having a test value 
    pk.generate()
    sig = hexlify(pk.sign(signThis).serialize())
    addr = script.p2pkh(pk.get_pubkey()).address()

    # res = {}
    # res['address'] = addr
    # res['sig'] = sig
    #write('/sd/PrepareVaultResponse.json, res)
    return [addr, sig, pk.get_pubkey()]

def FinalizeVault():
    '''
    Finalize Vault response
    reads the unsigned hex of the P2TST from the SD Card

    '''
    #data = json.loads(read('/sd/FinalizeVault.json'))
    # unvault_tx = Transaction.parse(unhexlify(data['txn'])) 
    # h = unvault_tx.sighash_legacy(0, script.p2pkh(pk.get_pubkey()))
    # sig = pk.sign(h)
    # unvault_tx.vin[0].script_sig = script.script_sig_p2pkh(sig, pk.get_pubkey())

    pk.delete() # delete the private key
    isDeleted = pk.key == None
    #txid = getTxid(unvault_tx)
    #PATH = '/flash/transactions/' + str(txid)
    #write(PATH, hexlify(unvault_tx.serialize()))) #saving P2TST to storage on board
    
    # #writing if key is deleted and the txid of P2TST
    #res = {}
    #res['isDeleted'] = isDeleted
    #res['txid'] = txid
    #PATH = '/sd/' + 'FinalizeVaultResponse.json'
    # #write(PATH, res)
    return isDeleted

def Unvault():
    # txid_list = json.loads(read('/sd/FinalizeVault.json'))['txids']
    # res = {}
    # for txid in txid_list:
    #     res[txid] = read('/flash/transactions/' + str(txid))
    #PATH = '/sd/' + 'UnvaultResponse.json'
    #write(PATH, res)
    return 0

def UnvaultRequest():
    txid_list = json.loads(read('/sd/FinalizeVault.json'))['txids']
    return txid_list

