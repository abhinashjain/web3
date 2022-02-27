# pip install py-solc-x

import os
import json
from solcx import compile_standard, install_solc
from web3 import Web3
from dotenv import load_dotenv

# load .env file in this code
# .env contains environment vairables such as private key
load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile our solidity code
install_solc("0.8.2")
compiled_solidity = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.2",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_solidity, file)


# get bytecode
bytecode = compiled_solidity["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# print(bytecode)

# get abi
abi = compiled_solidity["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]
# print(abi)

# connect to ganache, local blockchain node similar to Javascript VM in Remix
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# id of blockchain
chain_id = 1337

# wallet address and private key of contract's deployer or sender
# local test wallet
owner_address = "0xbd5a9466204Ad29E64bAE2295A99093aaa00Fb65"

# local test key
# for production don't harcode instead store this key in environment variable
private_key = os.getenv("PRIVATE_KEY")
# print(private_key)

# created the contract in python, using the contract written in solidity
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# print(SimpleStorage)

# get the total number of transaction done by owner address
nonce = w3.eth.getTransactionCount(owner_address)
# print(nonce)

print("Deployment started")
# To deploy the contract, we need 3 things:
# 1. build the transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": owner_address,
        "nonce": nonce,
    }
)  # construct here refers to SimpleStroage's contract in solidity
# 'to' address will be empty as we are sending to blockchain
# 'data' will be filled implicitly and contain the SimpleStroage contract. This data will have the abi and bytecode of our contract.

# print(transaction)

# 2. sign the transaction
signed_transaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)
# print(signed_transaction)

# 3. send the transaction
transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
# print(transaction_hash) # this hash is what we see in etherscan as "Transaction Hash"

# Wait for block confirmation
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
# print(transaction_receipt) # this will show "Transaction Hash", "Current Block Hash", and other relevant information as we see in etherscan

print("Deployment complete")

# Now, to work/interact with contract, we need 2 things:
# 1. contract address
# 2. contract ABI
SimpleStorage_contract = w3.eth.contract(
    address=transaction_receipt.contractAddress, abi=abi
)  # we can also use contract and abi of any other contract by getting its address and abi from its abis.py or abis.json file

# now, we can transact or interact with any funtion of this contract, using either of the two ways:
# 1. call (don't make state change in blockchain): good for calling 'view' (blue color in remix) type of functions
# 'call' is just a simulation, it doesn't change anything in blockchain
# 2. transact (does change the state): good for calling functions that changes the state (red and orange color in remix). this requires building and sending the transaction

# example of 'call'
print(SimpleStorage_contract.functions.retrieve().call())  # print '0'

# try changing number
print(SimpleStorage_contract.functions.store(15).call())

# still print '0', coz 'call' doesn't change anything in blockchain
print(SimpleStorage_contract.functions.retrieve().call())


print("Contract updation started")

# example of 'transact'
# change the value to 15 by building the transaction
store_transaction = SimpleStorage_contract.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": owner_address,
        "nonce": nonce + 1,
    }
)


# sign the transaction
signed_store_transaction = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)

# send the transaction
send_store_transaction = w3.eth.send_raw_transaction(
    signed_store_transaction.rawTransaction
)

# wait for confirmation
store_transaction_receipt = w3.eth.wait_for_transaction_receipt(send_store_transaction)

print("Contract updation end")

# now check the changed value as '15' using 'call'
print(SimpleStorage_contract.functions.retrieve().call())
