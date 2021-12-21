import click
from click.termui import prompt
import requests as r
# from requests import api
from tabulate import tabulate
import time as t
from Utilities.cryptography_testing import *
# import sys
# sys.path.insert(1, '/Wallet-App/Utilities')
# from Utilities import cryptography_testing
# from cryptography_testing import *
#Constants
SITE = 'localhost:8000/'
GET_CHAIN = f'{SITE}get_the_chain'
# MAKE_KEYS = f'{SITE}create_keys'
MINING = f'{SITE}mining'
CHECK_BALANCE = f'{SITE}check_balance'
MAKE_KEYS = Make_Keys()
# @click.command()

# def get_chain():
# 	""" gets chain """
# 	chain = r.get(GET_CHAIN).json()
# 	click.echo(chain)




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
def create_keys():
	""" pulls private key, password, and publickey """
	wallet = Make_Keys.make_spend_view_receive_keys()
	click.echo(f"\n \nPublic Key: {wallet['public spend key']}\n \nPrivate Key: {wallet['private spend key']}\n \nView key: {wallet['view key']}\n \nPrimary address: {wallet['primary address']}\n \nPassword For Wallet: {wallet['seed for wallet']}\n \nMessage: {wallet['message']}\n")


@click.command()
@click.option('--publickey', prompt='what is your publickey', help='provide your publickey')
def check_balance(publickey):
	""" checks the balance of a public key """
	data = {'publickey': publickey}
	data = r.post(CHECK_BALANCE, json=data)
	data = data.json()
	key = data['publickey']
	amount = data['balance']
	data = f'{key} has {amount} Tokens'
	click.echo(data)


@click.command()
@click.option('--publickey', prompt='what is your publickey', help='provide your publickey')
@click.option('--privatekey', prompt='what is your privatekey', help='provide your privatekey')
def mining(publickey, privatekey):
	""" mines blocks """
	stop = False
	data = {'publickey':publickey, 'privatekey':privatekey}
	request = r.post(MINING, json=data)
	if request.status_code == 200:
		while stop == False:
			t.sleep(1.0)
			request = r.post(MINING, json=data)
			table = []
			for re in request['message']:
				index = re['index']
				timestamp = re['timestamp']
				reward = re['amount'[publickey]]
				data = [index, timestamp, reward]
				table.append(data)
			click.echo(tabulate(table))
	else:
		return 'node must be down or invalid'


cli.add_command(get_chain)
cli.add_command(create_keys)
cli.add_command(mining)
cli.add_command(check_balance)



if __name__ == '__main__':
	cli()