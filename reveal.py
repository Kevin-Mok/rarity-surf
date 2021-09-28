import cache
import constants
import rarity

from pprint import pprint
from web3_api import getContract, getIPFSHash, getTokenMetadata, getTokenURI

TOKEN_NUM = 5
UNREVEALED_URI = f"QmSMahwiwLRNFnSzYKeHhbzLtqhbF8XzCGDoRxdzLqLFz6/{TOKEN_NUM}"

if __name__ == "__main__":
    token_uri = getTokenURI(getContract(), TOKEN_NUM)  
    ipfs_hash = getIPFSHash(token_uri)[-5:-2]
    print(ipfs_hash)
    print(not token_uri != UNREVEALED_URI)
