#include "main.h"

/****************** GUI classes ****************/

Label titleLbl;
Label dataLbl;

Button btn;
Label lbl;

/***************** Handler Classes ************ */
TrezorMessageHandler msg_handler = TrezorMessageHandler(); //message handler for protobuf
FSHandler fs_handler = FSHandler();

/***************** callback functions ***********/

void showInitScreen();
static lv_res_t constructTxCallback(lv_obj_t * btn);
static lv_res_t toInitMenuCallback(lv_obj_t * btn);
static lv_res_t showSerialCallback(lv_obj_t * btn);
static lv_res_t serialWriteCallback(lv_obj_t * btn);
static lv_res_t serialReadCallback(lv_obj_t * btn);

/************ bitcoin keys/locktimes ***********/

Tx txFinal;
uint8_t result[64];    //just to show the serial I/O working, do not actually need right now

/******************* Main part *****************/
int main(){
    init();
    fs_handler.init();
    showInitScreen();

    while(1){
        gui.update();
    }
}

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

    //construct p2tst
    Button btn2(constructTxCallback, "Construct P2TST");
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
    for(int i=0;i<64;i++) {
        sprintf(&(hexout[2*i]), "%02x", result[i]);
    }
    
    //sprintf(hexout, "msgtype=%d msglen=%ld", msg_handler.msgtype, msg_handler.msglen);
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

/****************** Callback Functions **************/

static lv_res_t toInitMenuCallback(lv_obj_t * btn){
    showInitScreen();
    return LV_RES_OK;
}

static lv_res_t constructTxCallback(lv_obj_t * btn){
    txFinal = constructTx();
    char file_name[128];
    sprintf(file_name, "%s%s%s", "fs/transactions/", txFinal.txid().c_str(), ".txt");
    //serial.printf("%s\n", (char*)file_name);
    //serial.printf("%s\n", (char*)txFinal.toString().c_str());
    serial.printf("%s\n", cscript.type());

    showTxnScreen();
    return LV_RES_OK;
}

static lv_res_t showSerialCallback(lv_obj_t * btn){
    showRead();
    return LV_RES_OK;
}

static lv_res_t serialWriteCallback(lv_obj_t * btn){
    //FIXME
    return LV_RES_OK;
}

static lv_res_t serialReadCallback(lv_obj_t * btn){

    // while( (res = handler.recv_data()) != 0 ){
    //     //keep reading
    // }
    //FIXME
    msg_handler.recv_data(result);
    gui.clear();
    gui.update();
    showRead();
    return LV_RES_OK;
}