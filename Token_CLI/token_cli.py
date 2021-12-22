import click
from click.termui import prompt
import requests as r
# from requests import api
from tabulate import tabulate
import time as t
from API.Utilities.cryptography_testing import *
from API.main import app
import uvicorn
from API.Utilities.encryption import Encrypt_and_Decrypt
import os
# import asyncio
from subprocess import run
# import sys
# sys.path.insert(1, '/Wallet-App/Utilities')
# from Utilities import cryptography_testing
# from cryptography_testing import *
#Constants
SERVER_NAME = 'Token Network'
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000
SERVER_RELOAD = False
SITE = 'http://localhost:8000/'
GET_CHAIN = f'{SITE}get_the_chain'
# MAKE_KEYS = f'{SITE}create_keys'
MINING = f'{SITE}mining'
CHECK_BALANCE = f'{SITE}check_balance'
TRANSACTIONS = f'{SITE}add_unconfirmed_transaction'
ADD_NODE = f'{SITE}add_node/'
MAKE_KEYS = Make_Keys()
ENCRYPT_AND_DECRYPT = Encrypt_and_Decrypt()
# @click.command()

# def get_chain():
# 	""" gets chain """
# 	chain = r.get(GET_CHAIN).json()
# 	click.echo(chain)


def run_app():
	uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, reload=SERVER_RELOAD)


@click.group()
def cli():
	pass

@click.command()
def get_chain():
	""" gets the chain """
	chains = r.get(GET_CHAIN).json()
	table = []
	for chain in chains['blockchain']:
		index = chain['index']
		timestamp = chain['timestamp']
		transaction = chain['data']
		# sender = None
		# receiver = None
		# amount = None
		if index != 1:
			i = 0
			while i < len(transaction):
				sender = chain['data'][i]['sender']
				receiver = chain['data'][i]['receiver']
				amount = chain['data'][i]['amount']
				data = [index, timestamp, sender, 'sent', amount, 'tokens', 'to', receiver]
				i = i + 1
		else:
			data = [index, timestamp, transaction[0]]

		table.append(data)
	# table = [['sun',2042740234017],['Earth',184018410347502]]
	click.echo(tabulate(table))


@click.command()
@click.option('--password', prompt='enter a password for your wallet', help='password protection for wallet')
@click.option('--file_name', prompt='enter the filename that you want to save your keys in', help='file name for wallet')
def create_keys(password, file_name):
	""" pulls private key, password, and publickey """
	wallet = Make_Keys().make_spend_view_receive_keys()
	public_spend = wallet['public spend key']
	private_spend = wallet['private spend key']
	view_key = wallet['view key']
	primary_address = wallet['primary address']
	seed = wallet['seed for wallet']
	key = password
	file = ENCRYPT_AND_DECRYPT.write_to_file(file_name, data=f'public spend key: {public_spend} \nprivate spend key: {private_spend} \nview key: {view_key} \nprimary address: {primary_address} \nwallet seed: {seed}')
	encrypt_file = ENCRYPT_AND_DECRYPT.encrypt_file(password=key, file=file)
	os.remove(file)
	click.echo(f"\n \nPublic Key: {wallet['public spend key']}\n \nPrivate Key: {wallet['private spend key']}\n \nView key: {wallet['view key']}\n \nPrimary address: {wallet['primary address']}\n \nSeed for wallet: {wallet['seed for wallet']} \n file containing wallet: {encrypt_file}")



@click.command()
@click.option('--password', prompt='password for wallet file', help='password for the wallet file')
@click.option('--file_name', prompt='enter the file name that contains the encrypted wallet with .encrypted at the end', help='file name for wallet')
def decrypt_wallet(password, file_name):
	""" decrypts the file containing your wallet """
	key = password
	decrypted_file = ENCRYPT_AND_DECRYPT.decrypt_file(password=key, encrypted_file=file_name)
	print(' ')
	print(' ')
	print(' ')
	click.echo(decrypted_file)


@click.command()
@click.option('--viewkey', prompt='what is your publickey', help='provide your publickey')
def check_balance(viewkey):
	""" checks the balance of a public key """
	data = {'publickey': viewkey}
	data = r.post(CHECK_BALANCE, json=data)
	data = data.json()
	key = data['Address']
	amount = data['balance']
	data = f'{key} has {amount} Tokens'
	click.echo(data)


@click.command()
@click.option('--primary_address', prompt='what is your primary address', help='provide your primary address')
def mining(primary_address):
	""" mines blocks """
	stop = False
	data = {'address':primary_address}
	request = r.post(MINING, json=data)
	if request.status_code == 200:
		while stop == False:
			t.sleep(0.5)
			request = r.post(MINING, json=data)
			table = []
			re = request.json()['message']
			index = re['index']
			timestamp = re['timestamp']
			previous_hash = re['previous_hash']
				# reward = re['amount']
			table_data = [index, previous_hash, timestamp]
			table.append(table_data)
			click.echo(tabulate(table))
	else:
		return 'node must be down or invalid! (make sure your node has started)'




@click.command()
@click.option('--public_spend_key', prompt='what is your public spend key', help='provide your public spend key')
@click.option('--private_spend_key', prompt='what is your private spend key', help='provide your private spend key')
@click.option('--view_key', prompt='what is your view key', help='provide your view key')
@click.option('--receiver', prompt="what is the receiver's primary address", help="provide the receiver's primary address")
@click.option('--amount', prompt='how many tokens would you like to send', help='provide the number of Tokens you want to send')
def transaction(public_spend_key, private_spend_key, view_key, receiver, amount):
	""" Makes transactions """
	data = {'sender_publickey': public_spend_key, 'sender_privatekey': private_spend_key, 'sender_public_viewkey': view_key, 'receiver': receiver, 'amount': amount}
	request = r.post(TRANSACTIONS, json=data)
	if request.status_code == 200:
		response = request['message']
	else:
		response = 'error, invalid response! (make sure your node has started)'
	click.echo(response)




click.command()
click.option('--node', prompt='enter the url for the node you want to add without https:// or without http://', help='add a node')
def add_node(node):
	""" add a node """
	data = {'node': node}
	request = r.post(ADD_NODE, json=data)
	if request.status_code == 200:
		response = 'node added successfully!'
	else:
		response = 'error, invalid response! (make sure your node has started)'



@click.command()
@click.option('--start', prompt='would you like to start the node (Y/n)', help='Starts the Node')
def start(start):
	'starts the node'
	if start == 'Y' or start == 'y':
		run_app()
		return 'Node has been started!'
	elif start == 'n' or start == 'N':
		return 'Node was not started!'
	else:
		return 'Invalid response, node was not started!'

cli.add_command(get_chain)
cli.add_command(create_keys)
cli.add_command(mining)
cli.add_command(check_balance)
cli.add_command(start)
cli.add_command(transaction)
cli.add_command(decrypt_wallet)


if __name__ == '__main__':
	cli()