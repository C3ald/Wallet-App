from passlib.hash import pbkdf2_sha256
import hashlib
import random
import base64
# import math
# import secrets
import string





# def make_stealth_keys(password):
# 	priv_key = hashlib.sha256(password).hexdigest()
# 	encoded_privkey = priv_key.encode()
# 	base64encoded_privkey = base64.b64encode(encoded_privkey)
# 	view_pubkey = pbkdf2_sha256.hash(str(base64encoded_privkey.decode()))
# 	print(view_pubkey)
# 	print(str(base64encoded_privkey.decode()))
class primary_addresses():
	""" makes your primary address for receiving Tokens and can verify it """
	def __init__(self):
		pass
	def make_primary_address(self, public_view):
		""" Makes the primary address and encodes it"""
		data = public_view
		encoded_data = data.encode()
		encoded_data = base64.b64encode(encoded_data)
		encoded_primary = hashlib.sha256(encoded_data).hexdigest()
		return encoded_primary


	def decode_primary_address(self,primary_address, public_view):
		data = public_view 
		encoded_data = data.encode()
		encoded_data = base64.b64encode(encoded_data)
		hashed_data = hashlib.sha256(encoded_data).hexdigest()
		if hashed_data == primary_address:
			return True
		else:
			return False




class Make_Keys():
	""" creates wallet keys or addresses """
	def __init__(self):
		pass

	def make_password(self):
		characters = string.ascii_letters + string.punctuation  + string.digits
		passwd =  "".join(random.choice(characters) for x in range(90))
		return str(passwd)


	def make_spend_view_recieve_keys(self, password:str):
		priv_spend = str(pbkdf2_sha256.hash(password))
		priv_spend = priv_spend.replace('$pbkdf2-sha256$29000$', '')
		pub_spend = str(pbkdf2_sha256.hash(priv_spend))
		pub_spend = pub_spend.replace('$pbkdf2-sha256$29000$', '')
		view_key = str(pbkdf2_sha256.hash(priv_spend))
		view_key = view_key.replace('$pbkdf2-sha256$29000$', '')
		prime_addr = primary_addresses().make_primary_address(view_key)
		return {'private spend key': priv_spend, 'public spend key': pub_spend, 'view key': view_key, 'receive address': prime_addr}

		# privkey_view = str(pbkdf2_sha256.hash(password))
		# privkey_view = privkey_view.replace('$pbkdf2-sha256$29000$', '')
		# pubkey_view = str(pbkdf2_sha256.hash(privkey_view))
		# pubkey_view = pubkey_view.replace('$pbkdf2-sha256$29000$', '')


		# priv_spend = str(pbkdf2_sha256.hash(password))
		# priv_spend = priv_spend.replace('$pbkdf2-sha256$29000$', '')
		# pub_spend = str(pbkdf2_sha256.hash(priv_spend))
		# pub_spend = pub_spend.replace('$pbkdf2-sha256$29000$', '')

		# return {'public view key':pubkey_view, 'private view key':privkey_view, 'public spend key': pub_spend, 'private sepend key': priv_spend}
	
	def make_stealth_keys(self, primary_address):
		stealth_address = str(pbkdf2_sha256.hash(primary_address))
		stealth_address = stealth_address.replace('$pbkdf2-sha256$29000$', '')
		return stealth_address

	
class Check_Wallet_Balance():
	""" Checks Balance and the validity of wallet addresses """
	def __init__(self):
		self.stealth_addresses = []
	def verify_stealth_keys(self, stealth_key, primary_address):
		full_stealth_address = '$pbkdf2-sha256$29000$'+stealth_key
		verify = pbkdf2_sha256.verify(primary_address, full_stealth_address)
		return verify
	
	def balance_check(self, public_view_key, blockchain):
		address = public_view_key
		chain = blockchain
		# i = 1
		# stealth_addresses = []
		# balance = 0
		# if i < len(blockchain):
		# 	while i != len(blockchain):
		# 		transactions = blockchain[i]['data']
		# 		for transaction in transactions:
		# 			receiver = transaction['receiver']
		# 			for address in stealth_addresses:
		# 				if receiver == address:
		# 					verify2 = False
		# 			verify = self.verify_stealth_keys(stealth_key=receiver, primary_address=primary_address)
		# 			if verify == True:
		# 				balance = balance + transaction['amount']
		# 				stealth_addresses.append(receiver)
		# 			sender = transaction['sender']

				# i = i + 1
		# decrypted_addr = primary_addresses().decode_primary_address(public_view=public_view_key, primary_address=primary_address)
		# if decrypted_addr == True:
		prime_addr = primary_addresses().make_primary_address(address)
		positive_balance = self.receiver_check(prime_addr, chain)
		negative_balance = self.sender_check(prime_addr, chain)
		balance = positive_balance - negative_balance
		return balance
		# else:
			# return 'invalid keys'

	def receiver_check(self, primary_address, blockchain):
		i = 1
		balance = 0
		if 1 < len(blockchain):
			while i != len(blockchain):
				transactions = blockchain[i]['data']
				for transaction in transactions:
					receiver = transaction['receiver']
					amount = transaction['amount']
					verify_wallet = self.verify_stealth_keys(receiver, primary_address)
					if verify_wallet == True:
						verify_double_spend = self.double_spend_check(stealth_key=receiver)
						if verify_double_spend == False:
							balance = balance + amount
				i = i + 1
		return balance


	def sender_check(self, sender_recieve_key, blockchain):
		i = 1
		balance = 0
		if 1 < len(blockchain):
			while i != len(blockchain):
				transactions = blockchain[i]['data']
				for transaction in transactions:
					sender = transaction['sender']
					amount = transaction['amount']
					verify_wallet = self.verify_stealth_keys(sender, sender_recieve_key)
					if verify_wallet == True:
						verify_double_spend = self.double_spend_check(stealth_key=sender)
						if verify_double_spend == False:
							balance = balance - amount
				i = i + 1
		return balance


				
	def double_spend_check(self, stealth_key, chain):
		self.stealth_addresses
		if len(chain) > 1:
			for addresses in self.stealth_addresses:
				if stealth_key == addresses:
					double_spend = True
					return double_spend
				else:
					double_spend = False
			if double_spend == False:
				self.stealth_addresses.append(stealth_key)
				return double_spend

	def verify_keys(self, publickey, privatekey):
		full_publickey = '$pbkdf2-sha256$29000$'+publickey
		# full_privatekey = '$pbkdf2-sha256$29000$'+privatekey
		verify = pbkdf2_sha256.verify(privatekey, full_publickey)
		return verify



if __name__ == '__main__'():
	primary_addresses()
	Check_Wallet_Balance()
	Make_Keys()
# make_stealth_keys()