'''
from bitcoin import script
from bitcoin import ec
from bitcoin.networks import NETWORKS
from ubinascii import unhexlify, hexlify
from deletedkey import *

#on board code
pk 		= DeletedKey()
pub 	= pk.get_pubkey()

PrepareVaultResponse: 
	addr 	= script.p2pkh(pk.get_pubkey())

serial.write([pk.sign(signThis), addr]) #do not need the redeem script it seems 
---
|

|
----

#on computer using pytohn-bitcoinlib 

from bitcoin import SelectParams
from bitcoin.core import b2x, lx, COIN, COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction, Hash160
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

SelectParams('mainnet')

# Create the (in)famous correct brainwallet secret key.
h = hashlib.sha256(b'correct horse battery staple').digest()
rec_seckey = CBitcoinSecret.from_secret_bytes(h)

lastblocktime = 1591836006
privkeys = {    
    'active'    :  makekey(b'Pippo3'),
    'clawback'  :  makekey(b'Pippo4'),
}

pubkeys = {x:privkeys[x].pub for x in privkeys}
scripts = { 
	#the script for the p2tst
    'staging_active':  CScript([
        OP_IF,
                lastblocktime, OP_NOP3, OP_DROP,
                pubkeys['active'], OP_CHECKSIGVERIFY,
        OP_ELSE,
                pubkeys['clawback'], OP_CHECKSIGVERIFY,
        OP_ENDIF])
}

#fake input for the vaulting txn
txid = lx('7e195aa3de827814f172c362fcf838d92ba10e3f9fdd9c3ecaf79522b311b22d')
vout = 0
txin = CMutableTxIn(COutPoint(txid, vout))

# We also need the scriptPubKey of the output we're spending because
# SignatureHash() replaces the transaction scriptSig's with it.
#
# Here we'll create that scriptPubKey from scratch using the pubkey that
# corresponds to the secret key we generated above.
txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(rec_seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])

#make a scriptPubKey out of the received address 
txout = CMutableTxOut(0.001*COIN, CBitcoinAddress(PrepareVaultResponse.addr).to_scriptPubKey())
tx = CMutableTransaction([txin], [txout])
# Calculate the signature hash for that transaction.
sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)

# Now sign it. We have to append the type of signature we want to the end, in
# this case the usual SIGHASH_ALL.
sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])

# Set the scriptSig of our transaction input appropriately.
txin.scriptSig = CScript([sig, seckey.pub])

# Verify the signature worked. This calls EvalScript() and actually executes
# the opcodes in the scripts to see if everything worked out. If it doesn't an
# exception will be raised.
VerifyScript(txin.scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))

# Done! Print the transaction to standard output with the bytes-to-hex
# function.
print(b2x(tx.serialize())) #the serialized version of the vaulting transaction


#working on the p2tst now
unvault_txid = lx(b2x(tx.GetTxid()))
vout = 0

unvault_txin = CMutableTxIn(COutPoint(unvault_txid, vout))
unvault_txout = CMutableTxOut(0.0005*COIN, scripts['staging_active'].to_p2sh_scriptPubKey())

unvault_tx = CMutableTransaction([unvault_txin], [unvault_txout])

#send FinalizeVault message
write(unvault_tx.serialize())

---
|

|
----

#back on board
unvault_tx = Transaction.parse(unhexlify(serial.read())) #reading the transaction from serial port
h = unvault_tx.sighash_legacy(0, script.p2pkh(pub))
sig = pk.sign(h)
unvault_tx.vin[i].script_sig = script.script_sig_p2pkh(sig, pub)

print(unvault_tx) #transaction is done 

pk.delete() # delete the private key
isDeleted = pk.key == None

FinalizeVaultResponse:
    isDeleted
    unvault_tx.txid

write_to_file(unvault_tx)

'''