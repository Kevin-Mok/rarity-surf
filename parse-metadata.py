import json 
import requests
import shutil
import urllib.request

from pprint import pprint
from web3 import Web3

ETHERSCAN_KEY = '2XEAQN2TAE7YABRYMR2HFEMCRXYUB9EDQC'
INFURA_PROJECT_ID = '1y5NJcmgstcJZ3CtveqhljSS3Tu'
INFURA_PROJECT_SECRET =                 'e02e9b9473b5e5198ba9be4400592182'

def getABI(contract_address):
    """Get ABI of contract using Etherscan's API.
    """
    ABI_json = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey=2XEAQN2TAE7YABRYMR2HFEMCRXYUB9EDQC"
    with urllib.request.urlopen(ABI_json) as url:
        data = json.loads(url.read().decode())
        return data["result"]

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
            auth=(INFURA_PROJECT_ID, INFURA_PROJECT_SECRET))

def downloadIPFSImage(imageIPFSHash, imagePath):
    """TODO: Docstring for downloadIPFSImage.

    :arg1: TODO
    :returns: TODO

    """
    params = (('arg', imageIPFSHash),)
    r = requests.post(
            'https://ipfs.infura.io:5001/api/v0/cat',
            params=params,
            auth=(INFURA_PROJECT_ID, INFURA_PROJECT_SECRET),
            stream=True)
    if r.status_code == 200:
        with open(imagePath, 'wb') as f:
            for chunk in r:
                f.write(chunk)

if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a57b116ee7a845a2ba0ee902a5280911'))
    contract_address = '0xf497253c2bb7644ebb99e4d9ecc104ae7a79187a'
    contract = w3.eth.contract(Web3.toChecksumAddress(contract_address), abi=getABI(contract_address))
    ipfsHash = getIPFSHash(getTokenURI(contract, 4629))
    metadata_json = json.loads(getIPFSResponse(ipfsHash).text)
    downloadIPFSImage(getIPFSHash(metadata_json["image"]), "./image")
