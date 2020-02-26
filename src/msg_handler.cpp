#include "msg_handler.h"
#include "main.h"

Serial serial(USBTX, USBRX);

int TrezorMessageHandler::send_data(uint8_t* buffer){

    serial.write(buffer, 64);
    return 0;
}

int TrezorMessageHandler::recv_data(uint8_t* buffer){
    serial.read(buffer, 64);
    //return 1;
    return unpack_data(buffer);

}

//unpack data from computer in 64 byte protobuf chunks
int TrezorMessageHandler::unpack_data(uint8_t buffer[64]) {
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
                initialize_handler();
                break;

            case hw_trezor_messages_MessageType_MessageType_PrepareVault:
                prepare_vault_handler();
                break;

            case hw_trezor_messages_MessageType_MessageType_FinalizeVault:
                finalize_vault_handler();
                break;

            case hw_trezor_messages_MessageType_MessageType_UnvaultRequest:
                unvault_handler();
                break;

            case hw_trezor_messages_MessageType_MessageType_CheckVaultBalance:
                check_vault_bal_handler();
                break;

            case hw_trezor_messages_MessageType_MessageType_CheckUnvaultBalance:
                check_unvault_bal_handler();
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

void TrezorMessageHandler::initialize_handler(){
    //initialize active/clawback xpubs into deletedlib

}

void TrezorMessageHandler::get_features_handler(){
    
    hw_trezor_messages_management_GetFeatures req      = hw_trezor_messages_management_GetFeatures_init_default;
    hw_trezor_messages_management_Features res         = hw_trezor_messages_management_Features_init_default;

    pb_istream_t stream_i = pb_istream_from_buffer(message, sizeof(message));
    pb_decode(&stream_i, hw_trezor_messages_management_GetFeatures_fields, &req);

    strncpy(res.vendor, "STMicroElectronics", 19);
    res.has_vendor = true;

    uint8_t response[sizeof(res)];
    pb_ostream_t stream_o = pb_ostream_from_buffer(response, sizeof(response));
    pb_encode(&stream_o, hw_trezor_messages_management_Features_fields, &res);
    pack_data(&stream_o, hw_trezor_messages_MessageType_MessageType_Features);

}

void TrezorMessageHandler::prepare_vault_handler(){
    hw_trezor_messages_bitcoin_PrepareVault req         = hw_trezor_messages_bitcoin_PrepareVault_init_default;
    hw_trezor_messages_bitcoin_PrepareVaultResponse res = hw_trezor_messages_bitcoin_PrepareVaultResponse_init_default;

    pb_istream_t stream_i = pb_istream_from_buffer(message, sizeof(message));
    pb_decode(&stream_i, hw_trezor_messages_bitcoin_PrepareVault_fields, &req);

    /* FIXME - add rest of vault preparation*/
}

void TrezorMessageHandler::finalize_vault_handler(){
    /* FIXME - add vault finalization*/

}

void TrezorMessageHandler::unvault_handler(){
    hw_trezor_messages_bitcoin_UnvaultRequest req         = hw_trezor_messages_bitcoin_UnvaultRequest_init_default;
    hw_trezor_messages_bitcoin_UnvaultResponse res        = hw_trezor_messages_bitcoin_UnvaultResponse_init_default;

    pb_istream_t stream_i = pb_istream_from_buffer(message, sizeof(message));
    pb_decode(&stream_i, hw_trezor_messages_bitcoin_UnvaultRequest_fields, &req);

    FILE *f = fs_handler.read((char*)req.txid);
    int size = fs_handler.get_size(f);

    fgets(res.hex, size, f);
    fs_handler.spend_close(f);

    uint8_t response[sizeof(res)];
    pb_ostream_t stream_o = pb_ostream_from_buffer(response, sizeof(response));
    pb_encode(&stream_o, hw_trezor_messages_bitcoin_UnvaultResponse_fields, &res);
    pack_data(&stream_o, hw_trezor_messages_MessageType_MessageType_UnvaultResponse);
}

void TrezorMessageHandler::check_vault_bal_handler(){

}

void TrezorMessageHandler::check_unvault_bal_handler(){

}

int TrezorMessageHandler::pack_data(pb_ostream_t *s, hw_trezor_messages_MessageType type){
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
