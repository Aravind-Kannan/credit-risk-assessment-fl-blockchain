import json
import ipfshttpclient
from web3 import Web3

def get_web3_provider(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]
    return web3

def upload_to_ipfs(filename):
    client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
    res = client.add(filename)
    print(res['Hash'])
    return res['Hash']

def get_model_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = config["contracts"]["model"]["ABI"]
    address = web3.toChecksumAddress(config["contracts"]["model"]["contractAddress"])

    contract = web3.eth.contract(address=address, abi=abi)
    return contract

def get_hash_storage_local_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = config["contracts"]["hashStorageLocal"]["ABI"]
    address = web3.toChecksumAddress(config["contracts"]["hashStorageLocal"]["contractAddress"])

    contract = web3.eth.contract(address=address, abi=abi)
    return contract

def get_hash_storage_global_contract(config):
    ganache_url = config["network_url"]
    web3 = Web3(Web3.HTTPProvider(ganache_url))

    web3.eth.defaultAccount = web3.eth.accounts[0]

    abi = config["contracts"]["hashStorageGlobal"]["ABI"]
    address = web3.toChecksumAddress(config["contracts"]["hashStorageGlobal"]["contractAddress"])

    contract = web3.eth.contract(address=address, abi=abi)
    return contract