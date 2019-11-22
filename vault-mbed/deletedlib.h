#ifndef __DELETEDLIB_H__
#define __DELETEDLIB_H__

// bitcoin lib
#include "Bitcoin.h"
#include "OpCodes.h"

// to use string class without std::
using namespace std;

Tx constructTx(long locktime, PublicKey active, PublicKey clawback, PrivateKey priv);

void deleteKey();

void constructScript(long locktime, PublicKey active, PublicKey clawback);




#endif