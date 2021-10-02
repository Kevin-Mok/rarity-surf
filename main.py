import cache
import constants
from math import ceil 
import rarity

from pprint import pprint
from web3_api import getContract, getIPFSHash, getTokenMetadata, getTokenURI

def cacheMetadataJSONS():
    master_json = cache.initMasterJSON()
    cache.cache_json(master_json, constants.MASTER_JSON_FILE)

    trait_counts = rarity.getTraitCounts(master_json)
    rarest_traits = rarity.calcRarestTraits(master_json, trait_counts)
    cache.cache_json(rarest_traits, constants.RARE_TRAITS_FILE)

    ranks = rarity.calcAllTokenScores(master_json)
    cache.cache_json(ranks, constants.RANKS_FILE)

    sorted_ranks = rarity.getSortedRanks(ranks)
    cache.cache_json(sorted_ranks, constants.SORTED_RANKS_FILE)

if __name__ == "__main__":
    #  contract = getContract()
    #  pprint(cache.createMasterJSON(contract, 1, 50))
    #  pprint(cache.getCachedTokens())
    #  pprint(cache.createMasterJSONThreaded(contract, 0, 100, 3))

    # step 1: cache metadata
    #  cache.cacheTokenMetadataThreaded(1, 5, 1)

    #  threads = ceil(constants.MAX_SUPPLY / 25)
    #  cache.cacheTokenMetadataThreaded(1, constants.MAX_SUPPLY, threads)

    # step 2
    cacheMetadataJSONS()
