from tkinter import *
from Token_CLI.API.Utilities.cryptography_testing import *
from Token_CLI.API.Utilities.encryption import Encrypt_and_Decrypt
encrypt_and_decrypt = Encrypt_and_Decrypt()
app = Tk()

makekeys = Make_Keys()
prime_address = primary_addresses()
verify_wallet = Check_Wallet_Balance()
""" The GUI wallet for the Token Network """
app.title('Token GUI Wallet')
app.geometry('300x300')


hiLabel = Label(app, text='The GUI Wallet for Token')
hiLabel.pack()
data = None
generate_wallet = Button(command=makekeys.make_spend_view_receive_keys(), text='click to make a wallet!')
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
