import cache
import constants
import rarity

from math import ceil 
from pprint import pprint
from web3_api import getContract, getIPFSHash, getTokenMetadata, getTokenURI

def cacheMetadataJSONS():
    #  master_json = cache.initMasterJSON()
    #  rarity.addNumberTraits(master_json)
    #  cache.cache_json(master_json, constants.MASTER_JSON_FILE)
    master_json = cache.read_json(constants.MASTER_JSON_FILE)

    #  trait_counts = rarity.getTraitCounts(master_json)
    #  cache.cache_json(trait_counts, constants.TRAIT_COUNTS_FILE)
    trait_counts = cache.read_json(constants.TRAIT_COUNTS_FILE)

    #  rarest_traits = rarity.calcRarestTraits(master_json, trait_counts)
    #  cache.cache_json(rarest_traits, constants.RARE_TRAITS_FILE)

    scores = rarity.calcTraitScores(master_json, trait_counts)
    cache.cache_json(scores, constants.SCORES_FILE)

    ranks = rarity.calcAllTokenScores(master_json)
    cache.cache_json(ranks, constants.RANKS_FILE)

    #  sorted_ranks = rarity.getSortedRanks(ranks)
    #  cache.cache_json(sorted_ranks, constants.SORTED_RANKS_FILE)

if __name__ == "__main__":
    #  contract = getContract()

    # step 1: cache metadata
    #  cache.cacheTokenMetadataThreaded(1, 5, 1)
    #  cache.cacheTokenMetadataThreaded(0, 0, 1)

    #  threads = ceil(constants.MAX_SUPPLY / 25)
    #  cache.cacheTokenMetadataThreaded(1, constants.MAX_SUPPLY, threads)

    # step 2
    #  cacheMetadataJSONS()
