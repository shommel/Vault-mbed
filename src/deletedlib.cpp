#include "deletedlib.h"

Script cscript;
Tx tx;
Signature sig;
PrivateKey delPriv;       
PublicKey clawback  = PrivateKey("Kzq8w6kkEXkWQN8CJSScLQfpkFUsJ6TqHHGBy1E6197byGahhDMb").publicKey();
PublicKey active    = PrivateKey("KzF2Wyvor6iyomL7svZTzf1RP7gNho8J3hmqAMg68HLiodhYFUmq").publicKey();
long locktime       = 9;

/*
'rec_staging':  CScript([
        OP_IF,
                lastblocktime, OP_NOP3, OP_DROP,
                pubkeys['staging'], OP_CHECKSIG,
        OP_ELSE,
                pubkeys['clawback'], OP_CHECKSIG,
        OP_ENDIF])
*/


PrivateKey test_private_key(){
	return delPriv;
}

PublicKey get_public_key(){
	return delPriv.publicKey();
}

void generateKey() { 
	uint8_t randomBuffer[32];
    //filling random buffer with 32 bytes 
    getRandomBuffer(randomBuffer, sizeof(randomBuffer));
    delPriv = PrivateKey(randomBuffer);
    for (int i = 0; i < 100; ++i){
    	bzero(randomBuffer, sizeof(randomBuffer));
    }

}

void deleteKey(){
	for (int i = 0; i < 100; ++i){
    	bzero(&delPriv, sizeof(delPriv));
    }
	
}

Tx constructTx(){
	tx = Tx();
	constructScript(locktime, active, clawback);

	// cscript = txin_redeemScript
	Script txin_scriptPubKey = cscript.scriptPubkey(); //returns p2sh script pubkey

	TxIn txin 	= TxIn("9058f16f9258ccc1bbb1f9cdeea47eadc7dab9fa346e2e15457bcf5369ca64a9", 0, 1);
	TxOut txout = TxOut(50, active.script());

	tx.addInput(txin);
	tx.addOutput(txout);

	Script rscript;
	rscript.push(OP_CHECKSIG);
	rscript.push(active);

	generateKey();
	sig = tx.signInput(0, delPriv, rscript);
	deleteKey();
	rscript.clear();

	return tx;
}

void constructScript(long locktime, PublicKey active, PublicKey clawback){
	cscript.clear();
	cscript.push(OP_ENDIF);
	cscript.push(OP_CHECKSIG);
	cscript.push(clawback);
	cscript.push(OP_ELSE);
	cscript.push(OP_CHECKSIG);
	cscript.push(active);
	cscript.push(OP_DROP);
	cscript.push(OP_CHECKSEQUENCEVERIFY);
	cscript.push(locktime);
	cscript.push(OP_IF);
}

