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

Script getScript();

Signature signMessage(uint8_t buf[32]);

void generateKey();

void deleteKey();

Tx constructTx(char* tx);

#endif