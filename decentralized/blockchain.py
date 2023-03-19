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
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"accuracy","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAccuracy","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLoss","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"loss","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_loss","type":"uint256"},{"internalType":"uint256","name":"_accuracy","type":"uint256"}],"name":"setMetrics","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    )
    address = web3.toChecksumAddress("0x2C440C3752d005A0494aD0A59001160f049645C1")

    contract = web3.eth.contract(address=address, abi=abi)
    return contract
