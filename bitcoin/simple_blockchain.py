#!/usr/bin/env python3

from hashlib import sha256
import json
import time

class Chain:
	def __init__(self):
		self.blockchain = []
		self.pending_transaction = []
		self.add_block(prevhash=1) #Genesis/first block

	def add_transaction(self, sender, recipient, amount):
		transaction = 	{	"sender": sender, 
					"recipient": recipient, 
					"amount": amount 
				}
		self.pending_transaction.append(transaction)

	def compute_hash(self, block):
		json_block = json.dumps(block, sort_keys=True).encode()
		hashed = sha256(json_block).hexdigest()
		return hashed

	def add_block(self, prevhash=None):
		block = {	"index": len(self.blockchain),
				"timestamp": time.time(),
				"transactions": self.pending_transaction,
				"proof": 0,
				"prevhash": prevhash or self.blockchain[-1]['currenthash'],
				"currenthash": 0
			}
		self.pending_transaction = []

		mining = self.compute_hash(block)
		while(mining[0] != '0'):
			block['proof'] += 1
			mining = self.compute_hash(block)
			
		block['currenthash'] = mining
		self.blockchain.append(block)

if __name__ == "__main__":
	chain = Chain()
	t1 = chain.add_transaction("Vitalik", "Satoshi", 100)
	t2 = chain.add_transaction("Satoshi", "Alice", 10)
	t3 = chain.add_transaction("Alice", "Charlie", 34)

	chain.add_block()

	t4 = chain.add_transaction("Bob", "Eve", 23)
	t5 = chain.add_transaction("Dennis", "Brian", 3)
	t6 = chain.add_transaction("Ken", "Doug", 88)

	chain.add_block()

	print(chain.blockchain)



'''
[{'index': 0, 'timestamp': 1645436898.4147737, 'transactions': [], 'proof': 8, 'prevhash': 1, 'currenthash': '032d8379b53214d57181cb5addd38f868133d464c12efbe4efab2a122d7a09ab'}, 

{'index': 1, 'timestamp': 1645436898.4149306, 'transactions': 
[{'sender': 'Vitalik', 'recipient': 'Satoshi', 'amount': 100}, 
{'sender': 'Satoshi', 'recipient': 'Alice', 'amount': 10}, 
{'sender': 'Alice', 'recipient': 'Charlie', 'amount': 34}], 'proof': 10, 'prevhash': '032d8379b53214d57181cb5addd38f868133d464c12efbe4efab2a122d7a09ab', 'currenthash': '0e299731a4279661b112e4d10c13edac5ab37c5ff088e8e82e65637f5b9e21b3'}, 

{'index': 2, 'timestamp': 1645436898.4151561, 'transactions': 
[{'sender': 'Bob', 'recipient': 'Eve', 'amount': 23}, 
{'sender': 'Dennis', 'recipient': 'Brian', 'amount': 3}, 
{'sender': 'Ken', 'recipient': 'Doug', 'amount': 88}], 'proof': 40, 'prevhash': '0e299731a4279661b112e4d10c13edac5ab37c5ff088e8e82e65637f5b9e21b3', 'currenthash': '0f887d57dbcb2bffc373ff36981792c962e9596b29515d27dd1d77424c3bc5a1'}]



'''









