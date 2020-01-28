#include "deletedlib.h"

Script cscript;
Tx tx;
Signature sig;
//uint8_t prev_id[32] = { "9058f16f9258ccc1bbb1f9cdeea47eadc7dab9fa346e2e15457bcf5369ca64a9" };

/*
'rec_staging':  CScript([
        OP_IF,
                lastblocktime, OP_NOP3, OP_DROP,
                pubkeys['staging'], OP_CHECKSIG,
        OP_ELSE,
                pubkeys['clawback'], OP_CHECKSIG,
        OP_ENDIF])
*/

void deleteKey(){
	
}

Tx constructTx(long locktime, PublicKey active, PublicKey clawback, PrivateKey priv){
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

	sig = tx.signInput(0, priv, rscript);
	return tx;
}

void constructScript(long locktime, PublicKey active, PublicKey clawback){
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

