from cryptography.fernet import Fernet
class Encrypt_and_Decrypt():
	""" Encryption and decryption of wallets to ensure security in the GUI wallet and while not in use with the GUI wallet """
	def __init__(self):
		self.password = None
	
	def write_key(self, filename):
		""" writes the key to a file """
		key = Fernet.generate_key()
		with open(f'{filename}.key', 'wb') as unlock:
			unlock.write(key)
		return {'message': f'your key is in {filename}'}

	def Encrypt_file(self, key, file):
		""" Encrypts the file's content """
		f = Fernet(key)
		with open(file, 'rb') as orginal_file:
			original = orginal_file.read()
		encrypted = f.encrypt(original)
	
	def Write_in_Encrypted_file(self, encryptedfile, key, data):
		""" Writes to the Encrypted file """
		f = Fernet(key)
		with open(encryptedfile, 'wb') as encrypted_file:
			encrypted_file.write(f.encrypt(data))
	
	def Decrypt_file(self, encryptedfile, key):
		""" Decrypts the Encrypted file's contents """
		f = Fernet(key)
		with open(encryptedfile, 'rb') as encrypted_file:
			encrypted = encrypted_file.read()
		decrypted = f.decrypt(encrypted)
		with open(decrypted, 'rb') as decrypted_file:
			decrypted_read = decrypted_file.read()
		return decrypted_read
	
if __name__ == '__main__':
	Encrypt_and_Decrypt()