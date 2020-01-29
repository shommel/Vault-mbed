#include <string>
#include <sstream>
#include <stdint.h>
#include <stdio.h>
#include "mbed.h"
#include <stdlib.h>
#include <chrono>
#include <thread>

// bitcoin/dev board headers
#include "Bitcoin.h"
#include "deletedlib.h"

// nanopb Headers
#include "messages-bitcoin.pb.h"
#include "messages-common.pb.h"
#include "messages.pb.h"
#include "messages-management.pb.h"
#include "pb_common.h"
#include "pb_decode.h"
#include "pb_encode.h"

/*
taken from https://github.com/trezor/trezor-common/blob/master/protob/protocol.md

First packet
--------|---------------|-------------------|-------------------------------------------|
offset    |    length         |    type             |        contents                            |
--------|---------------|-------------------|-------------------------------------------|
    0    |        3        |    char[3]            |        '?##' magic constant                |
--------|---------------|-------------------|-------------------------------------------|
    3    |        2        |    BE uint16_t        |        numerical message type                |
--------|---------------|-------------------|-------------------------------------------|
    5    |        4        |    BE uint32_t        |        message size                        |
--------|---------------|-------------------|-------------------------------------------|
    9    |        55        |    uint8_t[55]        |        first 55 bytes of message encoded     |
        |                |                    |        (padded w/ zeroes if need be)        |
--------|---------------|-------------------|-------------------------------------------|


Following packets
--------|---------------|-------------------|-------------------------------------------|
offset    |    length         |    type             |        contents                            |
--------|---------------|-------------------|-------------------------------------------|
    0    |        1        |    char[1]            |        '?' magic constant                    |
--------|---------------|-------------------|-------------------------------------------|
    1    |        63        |    uint8_t[63]        |        63 bytes of message encoded         |
        |                |                    |        (padded w/ zeroes if need be)        |
--------|---------------|-------------------|-------------------------------------------|                                                                            -

*/

Serial serial(USBTX, USBRX);

// __attribute__ packed
struct __attribute__ ((packed)) trezor_first_message { //structure of first protobuf packet above
    char header[3];
    uint16_t type;
    uint32_t size;
    uint8_t message[55];
};

struct __attribute__ ((packed)) trezor_subsequent_message { //structure of subsequent/following protobuf packet above
    char header;
    uint8_t message[63];
};

class TrezorMessageHandler {

    public:
        uint16_t msgtype; //type of message (look in messages.pb.h for list of types)
        uint32_t msglen = 0; // size of message
        uint8_t *message; //message w/o all protobuf headers
        uint32_t remainder; //remainder of message (if any) to be received in subsequent packets

        int send_data(uint8_t* buffer){

            serial.write(buffer, 64);
            return 0;
        }

        int recv_data(uint8_t* buffer){
            serial.read(buffer, 64);
            //return 1;
            return unpack_data(buffer);

        }

        //unpack data from computer in 64 byte protobuf chunks
        int unpack_data(uint8_t buffer[64]) {
            trezor_first_message* m = (trezor_first_message*)buffer;
            trezor_subsequent_message* n = (trezor_subsequent_message*)buffer;

            //check if message received is first packet
            //fill necessary fields
            if(string((char*)m->header) == "?##") {

                msgtype = m->type = __builtin_bswap16(m->type);
                msglen = m->size = __builtin_bswap32(m->size);
                message = (uint8_t *) malloc(msglen);
                memcpy(message, (buffer+9), min((uint32_t)55, msglen));
                remainder = msglen - min((uint32_t)55, msglen);

            //check if message received is subsequent packet
            //fill necessary fields
            } else if(n->header == '?') {

                //move the pointer to the current index to populate with remainder of message
                //if not, the original 55 bytes would be rewritten
                memcpy(message+(msglen - remainder), (buffer+1), min((uint32_t)63, remainder));
                remainder -= min((uint32_t)63, remainder);

            } else {
                // message error: header not recognized
            }

            if(remainder == 0) { // full message received

                // list of trezor message types found below
                // https://github.com/bitcoin-core/HWI/blob/master/hwilib/devices/trezorlib/messages/MessageType.py
                //call necessary message handler depending on message type received
                switch(msgtype) {

                    case hw_trezor_messages_MessageType_MessageType_DevBoardInitialize:
                        //initialize_handler(message);
                        break;

                    case hw_trezor_messages_MessageType_MessageType_GetPublicKey:
                        //get_pubkey_handler(message);
                        break;

                    case hw_trezor_messages_MessageType_MessageType_GetAddress:
                        //get_address_handler(message);
                        break;

                    case hw_trezor_messages_MessageType_MessageType_Vault:
                        //vault_handler(message);
                        break;

                    case hw_trezor_messages_MessageType_MessageType_Unvault:
                        //unvault_handler(message);
                        break;

                    case hw_trezor_messages_MessageType_MessageType_CheckVaultBalance:
                        //check_vault_bal_handler(message);
                        break;

                    case hw_trezor_messages_MessageType_MessageType_CheckUnvaultBalance:
                        //check_unvault_bal_handler(message);
                        break;

                    //called on initialization. respond with type 17 (features)
                    case hw_trezor_messages_MessageType_MessageType_GetFeatures:
                        get_features_handler();
                        break;

                    default :
                        break;
                        //message type error, message type not recognized
                }


                return 0; //full message received, tell the board to stop bugging cmp
            }

            return 1;
        }

        void initialize_handler(string m){
            //initialize active/clawback xpubs into deletedlib

        }

        void get_address_handler(string m){
            //initialize active/clawback xpubs into deletedlib

        }

        void get_features_handler(){
            //filling out with fake information
            //will get the information from somewhere else

			hw_trezor_messages_management_GetFeatures gf     = hw_trezor_messages_management_GetFeatures_init_default;
            hw_trezor_messages_management_Features f         = hw_trezor_messages_management_Features_init_default;

            pb_istream_t stream_i = pb_istream_from_buffer(message, sizeof(message));
            pb_decode(&stream_i, hw_trezor_messages_management_GetFeatures_fields, &gf);

            strncpy(f.vendor, "STMicroElectronics", 19);
            f.has_vendor = true;

            uint8_t response[sizeof(f)];
            pb_ostream_t stream_o = pb_ostream_from_buffer(response, sizeof(response));
            pb_encode(&stream_o, hw_trezor_messages_management_Features_fields, &f);
            pack_data(&stream_o, hw_trezor_messages_MessageType_MessageType_Features);

        }

        void get_pubkey_handler(string m){
            //PublicKey k = get_public_key();
            //pack_data(k.toString(), hw_trezor_messages_MessageType_MessageType_PublicKey);
        }

        void vault_handler(string m){
            //Tx txn = constructTx();
            //pack_data(txn.toString(), hw_trezor_messages_MessageType_MessageType_Vault);
            //print to screen
        }

        void unvault_handler(string m){

        }

        void check_vault_bal_handler(string m){

        }

        void check_unvault_bal_handler(string m){

        }

        int pack_data(pb_ostream_t *s, hw_trezor_messages_MessageType type){
        	//To come back to later
        	//pb_ostream has a field s->state that has the entirity of the message 
        		//from get_features_handler().
        	//Need to find a way to convert s->state into a buffer and iterate through
        		//its elements with the wile loop found in pack_data
        	//once done, also need to work on send_data function that will print 
        		//each of the 64 byte packets to the serial output
        	//Additionally, need to fix the little file system on board

        	//free(message); //we're done with this message, clearing it for next one
            trezor_first_message m;
            trezor_subsequent_message t;
            memset((void *)&m, '\0', 64); //dealing with padding if need be

            //filling first_message packet with header, type, size, message
            size_t msgsize = s->bytes_written;
            strncpy(m.header, "?##", 3);
            m.type = (uint16_t)type;
            m.size = msgsize;
            strncpy((char *)m.message, (char *)s->state, min((size_t)55, msgsize));
            msgsize -= min((size_t)55, msgsize); //determines if there is more message to pack

            uint8_t *buffer = (uint8_t*) malloc(sizeof(m));
            memcpy(buffer, &m, sizeof(m));
            send_data(buffer);

            //will pack rest of the message into subsequent packets
            while(msgsize > 0){
                memset((void *)&t, '\0', 64);
                t.header = '?';

                //copying either 63 bytes, or the remainder of message into t.message
                //strncpy((char*)t.message, s.substr(s.length() - msgsize, min((size_t)63, msgsize)).c_str(), min((size_t)63, msgsize));
				strncpy((char *)t.message, (char *)(uint8_t *)((s->state)+(m.size - msgsize)), min((size_t)63, msgsize));

                msgsize -= min((size_t)63, msgsize);

                memcpy(buffer, &t, sizeof(t));
                send_data(buffer);
            }

            free(buffer);

            return 0;
        }

        PrivateKey gui_test_key(){
            return test_private_key();
        }

        void gui_generate_key(){
            generateKey();
        }

};
