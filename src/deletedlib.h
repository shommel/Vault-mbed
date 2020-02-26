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

void deleteKey();



#endif