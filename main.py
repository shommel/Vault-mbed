import display
import pyb
from pyb import UART
import lvgl as lv
from MessageHandler import *

# def write_handler(obj, event):
#     if event == lv.EVENT.CLICKED:
#         uart.write('s'*64)

# def read_handler(obj, event):
#     if event == lv.EVENT.CLICKED:
#         l = uart.read(64)
#         uart.write(l)

def flush():
	if(uart.any() > 0):
		uart.read()

def read_handler(obj, event):
    if event == lv.EVENT.CLICKED:
        handler.read_data()

def flush_handler(obj, event):
    if event == lv.EVENT.CLICKED:
        flush()

#setting up UART comms FIXME: transition to USBHID 
uart = UART(3, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

#flushing out serial line upon init
flush()

handler = MessageHandler(uart)

display.init()
scr 	= lv.scr_act()

btn1 	= lv.btn(scr)
label1 = lv.label(btn1)
label1.set_text("flush")
btn1.set_width(100)
btn1.align(None, lv.ALIGN.IN_TOP_MID, 0, 0)
btn1.set_event_cb(flush_handler)

btn2 	= lv.btn(scr)
label2 = lv.label(btn2)
label2.set_text("read")
btn2.set_width(100)
btn2.align(None, lv.ALIGN.CENTER, 0, 0)
btn2.set_event_cb(read_handler)
