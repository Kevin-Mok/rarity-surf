#  from cache_data import cacheTokenMetadata, initMasterJSON
import cache_data
from web3_api import getContract

from pprint import pprint

if __name__ == "__main__":
    #  contract = getContract()
    #  cache_data.cacheTokenMetadata(contract, 4629, 4630)

    #  pprint(cache_data.initMasterJSON())
    #  cache_data.cacheMasterJSON(cache_data.initMasterJSON())
    pprint(cache_data.readMasterJSON()["4629"])
