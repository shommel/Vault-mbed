// mbed os headers
#include "mbed.h"

// bitcoin lib
#include "Bitcoin.h"
#include "PSBT.h"
#include "helpers.h"

// deleted key library
#include "deletedlib.h"

/****************** GUI classes ****************/

Label titleLbl;
Label dataLbl;

Button btn;
Label lbl;
Serial serial(USBTX, USBRX);  // tx, rx

/***************** GUI functions ***************/

void showInitScreen();
void showMenu();
static lv_res_t wipeCallback(lv_obj_t * btn);
static lv_res_t toVaultMenuCallback(lv_obj_t * btn);
static lv_res_t constructTxCallback(lv_obj_t * btn);
static lv_res_t toInitMenuCallback(lv_obj_t * btn);
static lv_res_t generateKeyCallback(lv_obj_t * btn);
static lv_res_t showAllKeysCallback(lv_obj_t * btn);
static lv_res_t writeTxToSdCallback(lv_obj_t * btn);
static lv_res_t showReadCallback(lv_obj_t * btn);
static lv_res_t serialWriteCallback(lv_obj_t * btn);
static lv_res_t serialReadCallback(lv_obj_t * btn);

/************ bitcoin keys/locktimes ***********/

PrivateKey delPriv;       
PublicKey clawback  = PrivateKey("Kzq8w6kkEXkWQN8CJSScLQfpkFUsJ6TqHHGBy1E6197byGahhDMb").publicKey();
PublicKey active    = PrivateKey("KzF2Wyvor6iyomL7svZTzf1RP7gNho8J3hmqAMg68HLiodhYFUmq").publicKey();
long locktime       = 9;
Tx txFinal;
int balance = 1;    //just to show the serial I/O working, do not actually need right now
uint8_t buffer[256];
size_t message_length;
bool status;

/******************* Main part *****************/
int main(){
    init();
    showInitScreen();

    while(1){
        gui.update();
    }
} 

/****************** GUI stuff *****************/

void showInitScreen(){
    gui.clear();
    titleLbl = Label("Welcome");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);  

    Button btn(showReadCallback, "Serial Part");
    btn.size(gui.width()-100, 80);
    btn.position(0, 100);
    btn.align(ALIGN_CENTER);

    Button btn1(generateKeyCallback, "Generate Key");
    btn1.size(gui.width()-100, 80);
    btn1.position(0, 200);
    btn1.align(ALIGN_CENTER);

    Button btn2(toVaultMenuCallback, "Prepare Vault Transaction");
    btn2.size(gui.width()-100, 80);
    btn2.position(0, 300);
    btn2.align(ALIGN_CENTER);

    Button btn3(writeTxToSdCallback, "Write P2TST to SD Card");
    btn3.size(gui.width()-100, 80);
    btn3.position(0, 400);
    btn3.align(ALIGN_CENTER);

    Button btn4(showAllKeysCallback, "Show all Keys");
    btn4.size(gui.width()-100, 80);
    btn4.position(0, 500);
    btn4.align(ALIGN_CENTER);

    Button btn5(wipeCallback, "Wipe device");
    btn5.size(gui.width()-100, 80);
    btn5.position(0, 600);
    btn5.align(ALIGN_CENTER);
}

void showMenu(){
    gui.clear();
    titleLbl = Label("What do you want to do?");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn(constructTxCallback, "Construct P2TST");
    btn.size(gui.width()-100, 80);
    btn.position(0, 200);
    btn.align(ALIGN_CENTER);

    Button btn2(toInitMenuCallback, "Back");
    btn2.size(gui.width()-100, 80);
    btn2.position(0, 300);
    btn2.align(ALIGN_CENTER);
}

void showKey(const string title, const string priv, const string pub){
    gui.clear();
    titleLbl = Label(title);
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("Priv: " + priv);
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 300);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("Pub: " + pub);
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 400);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn(toInitMenuCallback, "OK");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);
}

void showTBI(){
    gui.clear();
    titleLbl = Label("Constructing P2TST");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);  

    Button btn(toInitMenuCallback, "To Be Implemented");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);

    titleLbl = Label(txFinal.toString());
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 200);
    titleLbl.alignText(ALIGN_TEXT_CENTER);
}

void showAllKeys(){
    gui.clear();
    titleLbl = Label("Here's your private keys");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("Active public: " + active.toString());
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 300);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("clawback public: " + clawback.toString());
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 400);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("deleted key priv: " + delPriv.toString());
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 500);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("deleted key public: " + delPriv.publicKey().toString());
    dataLbl.size(gui.width()-100, 100);
    dataLbl.position(50, 600);
    dataLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn(toInitMenuCallback, "OK");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);
}

void showSDScreen(){
    gui.clear();
    titleLbl = Label("Saving to SD Card");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    Button btn(toInitMenuCallback, "OK");
    btn.size(gui.width()-100, 80);
    btn.position(0, gui.height()-100);
    btn.align(ALIGN_CENTER);
}

void showRead(){
    gui.clear();
    titleLbl = Label("Serial Port Communication");
    titleLbl.size(gui.width(), 20);
    titleLbl.position(0, 40);
    titleLbl.alignText(ALIGN_TEXT_CENTER);

    dataLbl = Label("Balance: " + to_string(balance));
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

/****************** Callback Stuff *****************/

static lv_res_t toInitMenuCallback(lv_obj_t * btn){
    showInitScreen();
    return LV_RES_OK;
}

static lv_res_t toVaultMenuCallback(lv_obj_t * btn){
    showMenu();
    return LV_RES_OK;
}

static lv_res_t constructTxCallback(lv_obj_t * btn){
    txFinal = constructTx(locktime, active, clawback, delPriv);
    showTBI();
    return LV_RES_OK;
}

static lv_res_t wipeCallback(lv_obj_t * btn){
    wipe();
    return LV_RES_OK;
}

static lv_res_t generateKeyCallback(lv_obj_t * btn){
    uint8_t randomBuffer[32];
    //filling random buffer with 32 bytes 
    getRandomBuffer(randomBuffer, sizeof(randomBuffer));
    delPriv = PrivateKey(randomBuffer);
    showKey("Here's your private key:", delPriv.toString(), delPriv.publicKey().toString());
    return LV_RES_OK;
}

static lv_res_t showAllKeysCallback(lv_obj_t * btn){
    showAllKeys();
    return LV_RES_OK;
}

static lv_res_t writeTxToSdCallback(lv_obj_t * btn){
    showSDScreen();
    return LV_RES_OK;
}

static lv_res_t showReadCallback(lv_obj_t * btn){
    showRead();
    return LV_RES_OK;
}

static lv_res_t serialWriteCallback(lv_obj_t * btn){
    const char *cstr = txFinal.toString().c_str();
    //serial.printf("%s\r", txFinal.toString());
    serial.printf("%s", cstr);
    return LV_RES_OK;
}

static lv_res_t serialReadCallback(lv_obj_t * btn){
    serial.scanf("%d", &balance);
    gui.clear();
    gui.update();
    showRead();
    return LV_RES_OK;
}
