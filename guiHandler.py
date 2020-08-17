import lvgl as lv
import pyb
import display
from fileHandler import *
from deletedKey import *
from transactionHandler import *
from messageHandler import *

class GUI:
	'''
	this class will be responsible for dealing with the gui/screen when buttons are pressed
	'''

	def __init__(self):
		self.display 	= display.init()
		self.scr 		= lv.scr_act()

	def clear(self):
		'''
		will reset the screen to blank it out 
		will be used inbetween switching gui screens
		'''
		self.scr.clean()


	'''
	GUI Functions
	'''
	def screenMainMenu(self):
		'''
		function to show the 'main menu' : screen shown on board booting up 
		'''
		self.clear()
		
		#welcome text at top of screen
		welcome_label = lv.label(self.scr)
		welcome_label.set_text("Welcome to Encumbered Cold Storage")
		welcome_label.align(None, lv.ALIGN.IN_TOP_MID, 0, 30)

		#Prepare Vault button
		btn1 	= lv.btn(self.scr)
		label1 = lv.label(btn1)
		label1.set_text("Test LED")
		btn1.set_width(120)
		btn1.set_x(180)
		btn1.set_y(220)
		btn1.set_event_cb(self.testLEDCb)

	def testLEDCb(self, obj, event):
		if event == lv.EVENT.CLICKED:
			pyb.LED(4).toggle()

		# #List P2TSTs button
		# btn5 	= lv.btn(self.scr)
		# label5 = lv.label(btn5)
		# label5.set_text("List P2TSTs")
		# btn5.set_width(120)
		# btn5.set_x(180)
		# btn5.set_y(520)
		# btn5.set_event_cb(self.listTxsCb)


'''
		#Prepare Vault button
		btn2 	= lv.btn(self.scr)
		label2 = lv.label(btn2)
		label2.set_text("Prepare Vault")
		btn2.set_width(120)
		btn2.set_x(180)
		btn2.set_y(220)
		btn2.set_event_cb(self.prepareVaultCb)

		#Finalize Vault button
		btn3 	= lv.btn(self.scr)
		label3 = lv.label(btn3)
		label3.set_text("Finalize Vault")
		btn3.set_width(120)
		btn3.set_x(180)
		btn3.set_y(320)
		btn3.set_event_cb(self.finalizeVaultCb)

		#Unvault button
		btn4 	= lv.btn(self.scr)
		label4 = lv.label(btn4)
		label4.set_text("Unvault")
		btn4.set_width(120)
		btn4.set_x(180)
		btn4.set_y(420)
		btn4.set_event_cb(self.unvaultRequestCb)

		#List P2TSTs button
		btn5 	= lv.btn(self.scr)
		label5 = lv.label(btn5)
		label5.set_text("List P2TSTs")
		btn5.set_width(120)
		btn5.set_x(180)
		btn5.set_y(520)
		btn5.set_event_cb(self.listTxsCb)

	def screenPrepareVault(self, res):
		self.clear()

		label = lv.label(self.scr)
		label.set_text("Prepare Vault")
		label.align(None, lv.ALIGN.IN_TOP_MID, 0, 30)

		result_label = lv.label(self.scr)
		result_label.set_text("Result:\tSuccess\nKey generated.\nAddress and signed authenticated message written to SDCard.")
		result_label.align(None, lv.ALIGN.CENTER, 0, -200)

		#setting up labels for the result of Prepare Vault function
		addr_label = lv.label(self.scr)
		addr_label.set_text(str("Address:    " + str(res[0])))
		addr_label.align(None, lv.ALIGN.CENTER, 0, 0)

		sig_label = lv.label(self.scr)
		sig_label.set_long_mode(lv.label.LONG.SROLL_CIRC)
		sig_label.set_width(300)
		sig_label.set_text(str("Signature:    " + str(res[1]) ))
		sig_label.align(None, lv.ALIGN.CENTER, 0, 80)

		pubkey_label = lv.label(self.scr)
		pubkey_label.set_long_mode(lv.label.LONG.SROLL_CIRC)
		pubkey_label.set_width(300)
		pubkey_label.set_text(str("Pubkey:    " + str(res[2]) ))
		pubkey_label.align(None, lv.ALIGN.CENTER, 0, 160)

		#button to return to the main menu 
		btn 	= lv.btn(self.scr)
		label2 = lv.label(btn)
		label2.set_text("Return to menu")
		btn.set_width(120)
		btn.align(None, lv.ALIGN.IN_BOTTOM_MID, 0, 0)
		btn.set_event_cb(self.mainMenuCb)

	def screenFinalizeVault(self, res):
		self.clear()

		label = lv.label(self.scr)
		label.set_text("Finalize Vault")
		label.align(None, lv.ALIGN.IN_TOP_MID, 0, 30)

		if res == True: #key is deleted. display success message
			result_label = lv.label(self.scr)
			result_label.set_text("Result: \t Success\nKey deleted. P2TST saved.\ntxid written to SDCard.")
			result_label.align(None, lv.ALIGN.CENTER, 0, 0)

		else:
			result_label = lv.label(self.scr)
			result_label.set_text("Result: \t Error\nKey not deleted.")
			result_label.align(None, lv.ALIGN.CENTER, 0, 0)

		#button to return to the main menu 
		btn 	= lv.btn(self.scr)
		label2 = lv.label(btn)
		label2.set_text("Return to menu")
		btn.set_width(120)
		btn.align(None, lv.ALIGN.IN_BOTTOM_MID, 0, 0)
		btn.set_event_cb(self.mainMenuCb)

	def screenUnvaultRequest(self):
		self.clear()

		label = lv.label(self.scr)
		label.set_text("Unvault Request")
		label.align(None, lv.ALIGN.IN_TOP_MID, 0, 30)

		result_label = lv.label(self.scr)
		result_label.set_text("Please confirm withdraw of the selected P2TSTs below")
		result_label.align(None, lv.ALIGN.IN_TOP_MID, 0, 100)

		

		#button to return to the main menu 
		btn 	= lv.btn(self.scr)
		label2 = lv.label(btn)
		label2.set_text("Confirm Unvault")
		btn.set_width(120)
		btn.align(None, lv.ALIGN.IN_BOTTOM_MID, 100, 0)
		btn.set_event_cb(self.confirmUnvaultCb)

		#button to return to the main menu 
		btn2 	= lv.btn(self.scr)
		label3 = lv.label(btn2)
		label3.set_text("Cancel Unvault")
		btn2.set_width(120)
		btn2.align(None, lv.ALIGN.IN_BOTTOM_MID, -100, 0)
		btn2.set_event_cb(self.mainMenuCb)

	def screenUnvaultConfirmation(self):
		self.clear()

		label = lv.label(self.scr)
		label.set_text("Unvault Confirmation")
		label.align(None, lv.ALIGN.IN_TOP_MID, 0, 30)

		result_label = lv.label(self.scr)
		result_label.set_text("Result:\tSuccess\nSelected P2TSTs written to SDCard.")
		result_label.align(None, lv.ALIGN.CENTER, 0, 0)

		#button to return to the main menu 
		btn 	= lv.btn(self.scr)
		label2 = lv.label(btn)
		label2.set_text("Return to menu")
		btn.set_width(120)
		btn.align(None, lv.ALIGN.IN_BOTTOM_MID, 0, 0)
		btn.set_event_cb(self.mainMenuCb)

	def screenListTxs(self):
		self.clear()

		label = lv.label(self.scr)
		label.set_text("List P2TSTs")
		label.align(None, lv.ALIGN.IN_TOP_MID, 0, 30)

		result_label = lv.label(self.scr)
		result_label.set_text("txid0, txid1, txid2, etc... \nTotal presigned txns:7\tAmount:2000834BTC")
		result_label.align(None, lv.ALIGN.CENTER, 0, 0)

		#button to return to the main menu 
		btn 	= lv.btn(self.scr)
		label2 = lv.label(btn)
		label2.set_text("Return to menu")
		btn.set_width(120)
		btn.align(None, lv.ALIGN.IN_BOTTOM_MID, 0, 0)
		btn.set_event_cb(self.mainMenuCb)


	Callback Functions


	def mainMenuCb(self, obj, event):
		if event == lv.EVENT.CLICKED:
			self.screenMainMenu()

	def prepareVaultCb(self, obj, event):
		if event == lv.EVENT.CLICKED:
			res = PrepareVault()
			self.screenPrepareVault(res)
		
	def finalizeVaultCb(self, obj, event):
		if event == lv.EVENT.CLICKED:
			res = FinalizeVault()
			self.screenFinalizeVault(res)

	def unvaultRequestCb(self, obj, event):
		if event == lv.EVENT.CLICKED:
			#res = UnvaultRequest()
			self.screenUnvaultRequest()

	def confirmUnvaultCb(self, obj, event):
		if event == lv.EVENT.CLICKED:
			res = Unvault()
			self.screenUnvaultConfirmation()

	def listTxsCb(self, obj, event):
		if event == lv.EVENT.CLICKED:
			#FIXME: list p2tst stuff
			self.screenListTxs()
'''
