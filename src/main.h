#ifndef MAIN_H
#define MAIN_H 

// mbed os headers
#include "mbed.h"

// bitcoin lib
#include "Bitcoin.h"
#include "helpers.h"
#include "deletedlib.h"

// handler librariers 
#include "msg_handler.h"
#include "fs_handler.h"

extern Serial serial;
extern FSHandler fs_handler;
extern TrezorMessageHandler msg_handler;

#endif