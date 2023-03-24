import json
import ipfshttpclient
from web3 import Web3

def get_web3_provider(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]
    return web3

def get_model_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = json.loads(
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accuracy","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"loss","type":"uint256"},{"indexed":false,"internalType":"string","name":"application","type":"string"}],"name":"ValuesUpdated","type":"event"},{"inputs":[],"name":"getAccuracy","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getApplication","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLoss","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"accuracy","type":"uint256"},{"internalType":"uint256","name":"loss","type":"uint256"},{"internalType":"string","name":"application","type":"string"}],"name":"setValues","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    )
    address = web3.toChecksumAddress("0x95F1929302B7C37660103Cc9f53aBeEAE71F3fB3")

    contract = web3.eth.contract(address=address, abi=abi)
    return contract

def upload_to_ipfs(filename):
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    res = client.add(filename)
    print(res['Hash'])
    return res['Hash']

def get_hash_storage_local_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = json.loads(
        '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"string","name":"hashValue","type":"string"},{"indexed":false,"internalType":"string","name":"application","type":"string"}],"name":"HashUpdated","type":"event"},{"inputs":[],"name":"_hashValue","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getApplication","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHash","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"hash","type":"string"},{"internalType":"string","name":"application","type":"string"}],"name":"storeHash","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    )
    address = web3.toChecksumAddress("0xA74Ca13Aaf6503C73864a8DfA4bcf24B53876575")

    contract = web3.eth.contract(address=address, abi=abi)
    return contract

def get_hash_storage_global_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = json.loads(
        '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"string","name":"hashValue","type":"string"},{"indexed":false,"internalType":"string","name":"application","type":"string"}],"name":"HashUpdated","type":"event"},{"inputs":[],"name":"_hashValue","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getApplication","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHash","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"hash","type":"string"},{"internalType":"string","name":"application","type":"string"}],"name":"storeHash","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    )
    address = web3.toChecksumAddress("0x6a9364078801ECFFcEc552C4F01F05F1902F30ac")

    contract = web3.eth.contract(address=address, abi=abi)
    return contract