#include "deletedlib.h"

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



string getAddress(){
	return delPriv.address();
}

PublicKey getPublicKey(){
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
