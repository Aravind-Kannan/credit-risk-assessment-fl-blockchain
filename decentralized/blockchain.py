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
        '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"accuracy","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"loss","type":"uint256"},{"indexed":false,"internalType":"string","name":"application","type":"string"}],"name":"ValuesUpdated","type":"event"},{"inputs":[],"name":"getAccuracy","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getApplication","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLoss","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"accuracy","type":"uint256"},{"internalType":"uint256","name":"loss","type":"uint256"},{"internalType":"string","name":"application","type":"string"}],"name":"setValues","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'
    )
    address = web3.toChecksumAddress("0x3CFdd17873bD4765f4b6328deE06F692aB32E0e0")

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
    address = web3.toChecksumAddress("0x499d3cA782E12E530a1cE0A55E14181dBbd45F07")

    contract = web3.eth.contract(address=address, abi=abi)
    return contract

def get_hash_storage_global_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = json.loads(
        '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"timestamp","type":"uint256"},{"indexed":false,"internalType":"string","name":"hashValue","type":"string"},{"indexed":false,"internalType":"string","name":"application","type":"string"}],"name":"HashUpdated","type":"event"},{"inputs":[],"name":"_hashValue","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getApplication","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getHash","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"hash","type":"string"},{"internalType":"string","name":"application","type":"string"}],"name":"storeHash","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    )
    address = web3.toChecksumAddress("0xaccFC90d28D3D3c3271b20675561CeDC6040F9D8")

    contract = web3.eth.contract(address=address, abi=abi)
    return contract