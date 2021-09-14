import json 
import os
from os.path import isfile, join, splitext
import requests
import shutil
import urllib.request

from pprint import pprint
from web3 import Web3

#  API keys {{{ # 

ETHERSCAN_KEY = '2XEAQN2TAE7YABRYMR2HFEMCRXYUB9EDQC'
WEB3_HTTP_PROVIDER = 'https://mainnet.infura.io/v3/a57b116ee7a845a2ba0ee902a5280911'
INFURA_IPFS_PROJECT_ID = '1y5NJcmgstcJZ3CtveqhljSS3Tu'
INFURA_IPFS_PROJECT_SECRET =                 'e02e9b9473b5e5198ba9be4400592182'

#  }}} API keys # 

# 7s
CONTRACT_ADDRESS = '0xf497253c2bb7644ebb99e4d9ecc104ae7a79187a'

CACHE_DIR = "./data/sevens"
RAW_CACHE_DIR = f"{CACHE_DIR}/raw"
MASTER_JSON_FILE = f"{CACHE_DIR}/master.json"

def getABI():
    """Get ABI of contract using Etherscan's API.
    """
    ABI_json = f"https://api.etherscan.io/api?module=contract&action=getabi&address={CONTRACT_ADDRESS}&apikey=2XEAQN2TAE7YABRYMR2HFEMCRXYUB9EDQC"
    with urllib.request.urlopen(ABI_json) as url:
        data = json.loads(url.read().decode())
        return data["result"]

def getContract():
    w3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))
    return w3.eth.contract(
            Web3.toChecksumAddress(CONTRACT_ADDRESS),
            abi=getABI())

def getTokenURI(contract, tokenId):
    """Get tokenURI from tokenId.
    """
    return contract.functions.tokenURI(tokenId).call()

def getIPFSHash(ipfsURL):
    return ipfsURL.removeprefix('ipfs://')

def getIPFSResponse(ipfsHash):
    params = (('arg',ipfsHash),)
    return requests.post(
            'https://ipfs.infura.io:5001/api/v0/cat',
            params=params,
            auth=(INFURA_IPFS_PROJECT_ID, INFURA_IPFS_PROJECT_SECRET))

def downloadIPFSImage(imageIPFSHash, imagePath):
    """
    Example usage:
    downloadIPFSImage(getIPFSHash(metadata_json["image"]),
        "./data/image")
    """
    params = (('arg', imageIPFSHash),)
    r = requests.post(
            'https://ipfs.infura.io:5001/api/v0/cat',
            params=params,
            auth=(INFURA_IPFS_PROJECT_ID, INFURA_IPFS_PROJECT_SECRET),
            stream=True)
    if r.status_code == 200:
        with open(imagePath, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def getTokenMetadata(contract, tokenNum):
    ipfsHash = getIPFSHash(getTokenURI(contract, tokenNum))
    return json.loads(getIPFSResponse(ipfsHash).text)

def cacheTokenMetadata(contract, startTokenNum, endTokenNum):
    for tokenNum in range(startTokenNum, endTokenNum + 1):
        tokenMetadata = getTokenMetadata(contract, tokenNum)
        with open(f"{RAW_CACHE_DIR}/{tokenNum}.json", 'w') as out:
            print(f"Caching Token #{tokenNum} to {out.name}:")
            pprint(tokenMetadata)
            json.dump(tokenMetadata, out, indent=2)

def getRawCacheFiles():
    return [file for file in os.listdir(RAW_CACHE_DIR) 
            if isfile(join(RAW_CACHE_DIR, file))]

def initMasterJSON():
    master_json = {}
    for file_name in getRawCacheFiles():
        with open(join(RAW_CACHE_DIR, file_name)) as json_file:
            master_json[file_name.removesuffix('.json')] = json.load(json_file)
    return master_json

def cacheMasterJSON(master_json):
    with open(MASTER_JSON_FILE, 'w') as out:
        json.dump(master_json, out, indent=2)

def readMasterJSON():
    with open(MASTER_JSON_FILE) as master_json:
        return json.load(master_json)

def updateMasterJSON(master_json, tokenNum, tokenData):
    pass

if __name__ == "__main__":
    #  contract = getContract()
    #  cacheTokenMetadata(contract, 4629, 4630)

    #  pprint(getFileList(RAW_CACHE_DIR))

    #  pprint(initMasterJSON())
    #  cacheMasterJSON(initMasterJSON())
    pprint(readMasterJSON()["4629"])
