import cache
import constants
from math import ceil 
import rarity

from pprint import pprint
from web3_api import getContract, getIPFSHash, getTokenMetadata, getTokenURI

if __name__ == "__main__":
    #  contract = getContract()
    #  cache.cacheTokenMetadata(contract, 1000, 1001)
    #  pprint(cache.createMasterJSON(contract, 1, 50))
    #  pprint(cache.getCachedTokens())

    # step 1
    #  cache.cacheTokenMetadataThreaded(1, 1000, 1000 // 25)
    #  threads = ceil(constants.MAX_SUPPLY / 25)
    #  cache.cacheTokenMetadataThreaded(1, constants.MAX_SUPPLY, threads)

    # step 2
    cache.cache_json(cache.initMasterJSON(), constants.MASTER_JSON_FILE)

    # step 3
    master_json = cache.read_json(constants.MASTER_JSON_FILE)
    trait_counts = rarity.getTraitCounts(master_json)
    rarest_traits = rarity.calcRarestTraits(master_json, trait_counts)
    cache.cache_json(rarest_traits, constants.RARE_TRAITS_FILE)
    cache.cache_json(rarity.calcAllTokenScores(master_json),
            constants.RANKS_FILE)

    #  pprint(cache.createMasterJSONThreaded(contract, 0, 100, 3))
