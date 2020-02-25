#ifndef __DELETEDLIB_H__
#define __DELETEDLIB_H__

// bitcoin lib
#include "Bitcoin.h"
#include "OpCodes.h"


#include "helpers.h"

// to use string class without std::
using namespace std;

string getAddress();

PublicKey getPublicKey();

void generateKey();

Tx constructTx(Tx tx, uint32_t value);

void deleteKey();

void constructScript(long locktime, PublicKey active, PublicKey clawback);



#endif