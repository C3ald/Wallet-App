from tkinter import *
from Utilities.wallet import Wallet
from Utilities.encryption import Encrypt_and_Decrypt
encrypt_and_decrypt = Encrypt_and_Decrypt()
wallet = Wallet()
app = Tk()


""" The GUI wallet for the Token Network """
app.title('Token GUI Wallet')
app.geometry('300x300')


hiLabel = Label(app, text='The GUI Wallet for Token')
hiLabel.pack()

generate_wallet = Button(command=wallet.make_wallet(), text='click to make a wallet!')
generate_wallet.pack()
# menu = Menubutton(app, text='menu')
# menu.menu = Menu(menu)
# menu["menu"] = menu.menu

# label = Label(app, text="hello world")

# label.pack()



# def WalletCreation():
# 	mywallet = wallet.make_wallet()
# 	print(mywallet)

# button = Button(app, text='Click Me', command=WalletCreation)
# button.pack()














app.mainloop()
