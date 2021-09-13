from web3 import Web3
import urllib.request, json 
from pprint import pprint
import requests

ETHERSCAN_KEY = '2XEAQN2TAE7YABRYMR2HFEMCRXYUB9EDQC'

def getABI(contract_address):
    """Get ABI of contract using Etherscan's API.
    """
    ABI_json = f"https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey=2XEAQN2TAE7YABRYMR2HFEMCRXYUB9EDQC"
    with urllib.request.urlopen(ABI_json) as url:
        data = json.loads(url.read().decode())
        return data["result"]

def getTokenURI(contract, tokenId):
    return contract.functions.tokenURI(tokenId).call()

def getIPFSHash(ipfsURL):
    return ipfsURL.removeprefix('ipfs://')

if __name__ == "__main__":
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a57b116ee7a845a2ba0ee902a5280911'))
    contract_address = '0xf497253c2bb7644ebb99e4d9ecc104ae7a79187a'
    contract = w3.eth.contract(Web3.toChecksumAddress(contract_address), abi=getABI(contract_address))
    ipfsHash = getIPFSHash(getTokenURI(contract, 4629))
    params = (('arg',ipfsHash),)
    response = requests.post(
            'https://ipfs.infura.io:5001/api/v0/cat',
            params=params,
            auth=('1y5NJcmgstcJZ3CtveqhljSS3Tu',
                'e02e9b9473b5e5198ba9be4400592182'))
    metadata_json = json.loads(response.text)
    print(metadata_json["image"])
