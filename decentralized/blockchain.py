import json
from web3 import Web3

def get_web3_provider(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]
    return web3

def get_metrics_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accuracy","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"loss","type":"uint256"}],"name":"ValuesUpdated","type":"event"},{"inputs":[],"name":"getAccuracy","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLoss","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"accuracy","type":"uint256"},{"internalType":"uint256","name":"loss","type":"uint256"}],"name":"setValues","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    )
    address = web3.toChecksumAddress("0xACEf0eB79189634ABe691d4031648450f9c9e2bb")

    contract = web3.eth.contract(address=address, abi=abi)
    return contract
