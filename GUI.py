from tkinter import *

from asyncio.tasks import wait_for
from API.Utilities.cryptography_testing import *
from API.Utilities.encryption import Encrypt_and_Decrypt
from API.main import app
import uvicorn
import multiprocessing
import time as t
import subprocess

encrypt_and_decrypt = Encrypt_and_Decrypt()


class ButtonCommands():
	def __init__(self):
		pass

	def openWallet(self):
		subprocess.Popen(r'explorer /select, "C:\"')


class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.pack(fill=BOTH, expand=1)
		openwalletButton = Button(self, text='locate wallet', command=ButtonCommands().openWallet)
		openwalletButton.place(x=0, y=0)

root = Tk()
guiapp = Window(root)
root.wm_title('Token GUI Wallet')
root.geometry('640x400')


def startAPI():
	uvicorn.run(app, host='0.0.0.0', port=5000, reload=False)

def startGUI():
	root.mainloop()

# def stopProcesses():











if __name__ == '__main__':
	GUI = multiprocessing.Process(name='GUI', target=startGUI)
	GUI.start()
	API = multiprocessing.Process(name='API',target=startAPI)
	API.start()
	while True:
		if GUI.is_alive() == True and API.is_alive() == True:
			pass
		
		if GUI.is_alive() == False:
			API.kill()
			break


		if API.is_alive() == False:
			GUI.kill()
			break






