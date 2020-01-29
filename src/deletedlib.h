#ifndef __DELETEDLIB_H__
#define __DELETEDLIB_H__

// bitcoin lib
#include "Bitcoin.h"
#include "OpCodes.h"


#include "helpers.h"

// to use string class without std::
using namespace std;

PublicKey get_public_key();

PrivateKey test_private_key();

void generateKey();

Tx constructTx();

void deleteKey();

void constructScript(long locktime, PublicKey active, PublicKey clawback);



#endif