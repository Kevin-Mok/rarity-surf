import cache
import constants
import rarity

from pprint import pprint
from web3_api import getContract, getIPFSHash, getTokenMetadata, getTokenURI

TOKEN_NUM = 1
UNREVEALED_URI = f"QmSMahwiwLRNFnSzYKeHhbzLtqhbF8XzCGDoRxdzLqLFz6/{TOKEN_NUM}"

if __name__ == "__main__":
    contract = getContract(constants.HEARTS_CONTRACT_ADDRESS)
    token_uri = getTokenURI(contract, TOKEN_NUM)  
    ipfs_hash = getIPFSHash(token_uri)[-5:-2]
    print(ipfs_hash)
    print(token_uri != UNREVEALED_URI)
