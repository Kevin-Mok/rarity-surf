import constants

import json 
import requests
import urllib.request
from web3 import Web3

ETHERSCAN_KEY = '2XEAQN2TAE7YABRYMR2HFEMCRXYUB9EDQC'
WEB3_HTTP_PROVIDER = 'https://mainnet.infura.io/v3/a57b116ee7a845a2ba0ee902a5280911'
INFURA_IPFS_PROJECT_ID = '1y5NJcmgstcJZ3CtveqhljSS3Tu'
INFURA_IPFS_PROJECT_SECRET = 'e02e9b9473b5e5198ba9be4400592182'

SEVENS_CONTRACT_ADDRESS = '0xf497253c2bb7644ebb99e4d9ecc104ae7a79187a'
SEVENS_IPFS_HASH = "QmRE9x8qTTRtvS3UxDtzMCVV9GJKBfD8TgUoym1ePireGU"

def getABI():
    """Get ABI of contract using Etherscan's API.
    """
    ABI_json = f"https://api.etherscan.io/api?module=contract&action=getabi&address={SEVENS_CONTRACT_ADDRESS}&apikey={ETHERSCAN_KEY}"
    with urllib.request.urlopen(ABI_json) as url:
        data = json.loads(url.read().decode())
        return data["result"]

def getContract():
    w3 = Web3(Web3.HTTPProvider(WEB3_HTTP_PROVIDER))
    return w3.eth.contract(
            Web3.toChecksumAddress(constants.SEVENS_CONTRACT_ADDRESS),
            abi=getABI())

def getTokenURI(contract, tokenId):
    """Get tokenURI from tokenId.
    """
    return contract.functions.tokenURI(tokenId).call()

#  def getTokenMetadata(contract, tokenNum):
def getTokenMetadata(tokenNum):
    #  ipfsHash = getIPFSHash(getTokenURI(contract, tokenNum))
    #  return json.loads(getIPFSResponse(ipfsHash).text)
    return json.loads(
            getIPFSResponse(f"{SEVENS_IPFS_HASH}/{tokenNum}").text)

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

