from tkinter import *

from asyncio.tasks import wait_for
from API.Utilities.cryptography_testing import *
from API.Utilities.encryption import Encrypt_and_Decrypt
from API.main import app
import uvicorn
import multiprocessing
import time as t

encrypt_and_decrypt = Encrypt_and_Decrypt()
class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master

root = Tk()
app = Window(root)
root.wm_title('Token GUI Wallet')



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






