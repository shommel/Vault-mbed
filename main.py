from GuiHandler import *
from FileHandler import initTxnDir

#initializing transactions dir if it does not already exist
initTxnDir()

#initializes gui object and the 'main menu'
gui = GUI() 
gui.screenMainMenu()

