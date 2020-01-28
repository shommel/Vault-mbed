// mbed os headers
#include "mbed.h"
#include "BlockDevice.h"
#include "LittleFileSystem.h"

// bitcoin lib
#include "Bitcoin.h"
#include "PSBT.h"
#include "helpers.h"

// deleted key library
#include "deletedlib.h"

// nanopb handler library
#include "handler.h"

/****************** GUI classes ****************/

Label titleLbl;
Label dataLbl;

Button btn;
Label lbl;
TrezorMessageHandler handler = TrezorMessageHandler(); //message handler for protobuf
//BlockDevice *bd = BlockDevice::get_default_instance();
BlockDevice *bd = BlockDevice::get_default_instance();
LittleFileSystem fs("fs");

/***************** callback functions ***********/

void showInitScreen();
static lv_res_t wipeCallback(lv_obj_t * btn);
static lv_res_t constructTxCallback(lv_obj_t * btn);
static lv_res_t showAllKeysCallback(lv_obj_t * btn);
static lv_res_t toInitMenuCallback(lv_obj_t * btn);
static lv_res_t showSerialCallback(lv_obj_t * btn);
static lv_res_t serialWriteCallback(lv_obj_t * btn);
static lv_res_t serialReadCallback(lv_obj_t * btn);
static lv_res_t generateKeyCallback(lv_obj_t * btn);
static lv_res_t fileCallback(lv_obj_t * btn);
static lv_res_t readFileCallback(lv_obj_t * btn);
static lv_res_t writeFileCallback(lv_obj_t * btn);
static lv_res_t unmountCallback(lv_obj_t * btn);

//initiailize, getfeatures, and features

/************ bitcoin keys/locktimes ***********/

Tx txFinal;
uint8_t result[64];    //just to show the serial I/O working, do not actually need right now
char test_buffer[100];
int file_test = 0;

/******************* Main part *****************/
int main(){

    fs.mount(bd);

    init();
    showInitScreen();

    while(1){
        gui.update();
    }
}

/****************** GUI stuff *****************/

//initial screen on dev board start up
void showInitScreen(){

    gui.clear();
    titleLbl = Label("Welcome");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    //serial communication part for testing
    Button btn(showSerialCallback, "Serial Port");
    btn.size(gui.width()-100, 80);
    btn.position(0, 100);
    btn.align(ALIGN_CENTER);

    Button btn3(showAllKeysCallback, "Show all Keys");
    btn3.size(gui.width()-100, 80);
    btn3.position(0, 200);
    btn3.align(ALIGN_CENTER);

    //construct p2tst
    Button btn2(constructTxCallback, "Construct P2TST");
    btn2.size(gui.width()-100, 80);
    btn2.position(0, 300);
    btn2.align(ALIGN_CENTER);

    Button btn5(generateKeyCallback, "Generate Key");
    btn5.size(gui.width()-100, 80);
    btn5.position(0, 400);
    btn5.align(ALIGN_CENTER);

    //method of 'deleting' private key
    Button btn4(wipeCallback, "Wipe device");
    btn4.size(gui.width()-100, 80);
    btn4.position(0, 500);
    btn4.align(ALIGN_CENTER);

    Button btn6(fileCallback, "File System Test");
    btn6.size(gui.width()-100, 80);
    btn6.position(0, 600);
    btn6.align(ALIGN_CENTER);
}

void showMenu(){
    gui.clear();
    titleLbl = Label("What do you want to do?");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn2(toInitMenuCallback, "Back");
    btn2.size(gui.width()-100, 80);
    btn2.position(0, 300);
    btn2.align(ALIGN_CENTER);
}

//display transaction hex on screen (for testing purposes)
void showTxnScreen(){
    gui.clear();

    titleLbl = Label("Raw P2TST Bitcoin Transaction Hex");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn(toInitMenuCallback, "OK");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);

    titleLbl = Label(txFinal.toString().c_str());
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 200);
    titleLbl.alignText(ALIGN_TEXT_CENTER);
}


//serial I/O testing screen
void showRead() {
    gui.clear();
    titleLbl = Label("Serial Port Communication");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    char hexout[129];
    
    hexout[128] = '\0';
    // for(int i=0;i<64;i++) {
    //     sprintf(&(hexout[2*i]), "%02x", result[i]);
    // }
    
    sprintf(hexout, "msgtype=%d msglen=%d", handler.msgtype, handler.msglen);
    dataLbl = Label(string("[") + hexout + string("]"));
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 100);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn2(serialWriteCallback, "Write to Serial Port");
    btn2.size(gui.width()-100, 80);
    btn2.position(0, gui.height()-300);
    btn2.align(ALIGN_CENTER);

    Button btn3(serialReadCallback, "Read from Serial Port");
    btn3.size(gui.width()-100, 80);
    btn3.position(0, gui.height()-200);
    btn3.align(ALIGN_CENTER);

    Button btn(toInitMenuCallback, "OK");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);
}

void showAllKeys(){
    gui.clear();

    PrivateKey priv = handler.gui_test_key();
    titleLbl = Label("Here's your private keys");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("deleted key priv: " + priv.toString());
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 500);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("deleted key public: " + priv.publicKey().toString());
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 600);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn(toInitMenuCallback, "OK");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);
}

void showFileScreen(){
    gui.clear();

    titleLbl = Label("Testing MBED-OS File System");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn1(readFileCallback, "Read from File");
    btn1.size(gui.width()-100, 80);
    btn1.position(0, 200);
    btn1.align(ALIGN_CENTER);

    Button btn2(writeFileCallback, "Write to File");
    btn2.size(gui.width()-100, 80);
    btn2.position(0, 300);
    btn2.align(ALIGN_CENTER);

    titleLbl = Label((char*)test_buffer);
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 400);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn3(unmountCallback, "Unmount");
    btn3.size(gui.width()-100, 80);
    btn3.position(0, gui.height()-200);
    btn3.align(ALIGN_CENTER);

    Button btn(toInitMenuCallback, "OK");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);
}

/****************** Callback Stuff *****************/

static lv_res_t generateKeyCallback(lv_obj_t * btn){
    handler.gui_generate_key();
    return LV_RES_OK;
}

static lv_res_t showAllKeysCallback(lv_obj_t * btn){
    showAllKeys();
    return LV_RES_OK;
}

static lv_res_t toInitMenuCallback(lv_obj_t * btn){
    showInitScreen();
    return LV_RES_OK;
}

static lv_res_t constructTxCallback(lv_obj_t * btn){
    txFinal = constructTx();
    showTxnScreen();
    return LV_RES_OK;
}

static lv_res_t wipeCallback(lv_obj_t * btn){
    wipe();
    return LV_RES_OK;
}

static lv_res_t showSerialCallback(lv_obj_t * btn){
    showRead();
    return LV_RES_OK;
}

static lv_res_t serialWriteCallback(lv_obj_t * btn){
    //FIXME
    serial.write("hello", 6);
    //handler.get_features_handler();
    return LV_RES_OK;
}

static lv_res_t serialReadCallback(lv_obj_t * btn){

    // while( (res = handler.recv_data()) != 0 ){
    //     //keep reading
    // }
    //FIXME
    handler.recv_data(result);
    gui.clear();
    gui.update();
    showRead();
    return LV_RES_OK;
}

static lv_res_t fileCallback(lv_obj_t * btn){

    showFileScreen();
    return LV_RES_OK;

}

static lv_res_t readFileCallback(lv_obj_t * btn){
    FILE *f = fopen("/fs/p2tst1.txt", "r");
    fgets(test_buffer, 100, f);
    fclose(f);
    showFileScreen();
    return LV_RES_OK;
}

static lv_res_t writeFileCallback(lv_obj_t * btn){
    FILE *f = fopen("/fs/p2tst1.txt", "w");
    fprintf(f, "%s\n", to_string(file_test++).c_str());
    fflush(f);
    fclose(f);
    showFileScreen();
    return LV_RES_OK;
}

static lv_res_t unmountCallback(lv_obj_t * btn){
    fs.unmount();
    showFileScreen();
    return LV_RES_OK;

}





