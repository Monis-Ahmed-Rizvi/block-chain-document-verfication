import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# Connect to local Ethereum node (Ganache)
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Load contract ABI
current_dir = os.path.dirname(os.path.abspath(__file__))
blockchain_dir = os.path.join(current_dir, '..', '..', 'blockchain')
compiled_contract_path = os.path.join(blockchain_dir, 'build', 'contracts', 'DocumentVerification.json')

with open(compiled_contract_path, 'r') as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

# Get contract address from environment variable
contract_address = os.getenv('CONTRACT_ADDRESS')

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def add_to_blockchain(document_hash):
    try:
        account = w3.eth.accounts[0]
        tx_hash = contract.functions.addDocument(document_hash).transact({'from': account})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.transactionHash.hex()
    except Exception as e:
        print(f"Error adding to blockchain: {str(e)}")
        return None

def verify_on_blockchain(document_hash):
    try:
        return contract.functions.verifyDocument(document_hash).call()
    except Exception as e:
        print(f"Error verifying on blockchain: {str(e)}")
        return False