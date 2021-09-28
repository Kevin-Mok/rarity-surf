import cache
from constants import MASTER_JSON_FILE, RANKS_FILE, SCORES_FILE 
import rarity

from pprint import pprint
from web3_api import getContract, getTokenMetadata

if __name__ == "__main__":
    #  contract = getContract()
    #  cache.cacheTokenMetadata(contract, 1000, 1001)
    #  pprint(cache.createMasterJSON(contract, 1, 50))
    cache.cacheTokenMetadataThreaded(0, 100, 100)
    #  pprint(getTokenMetadata(123))

    #  pprint(cache.initMasterJSON())
    #  TODO: test new general cache fxns # 
    #  cache.cacheMasterJSON(cache.initMasterJSON())
    #  cache.cache_json(cache.initMasterJSON(), MASTER_JSON_FILE)
    #  pprint(cache.read_json(MASTER_JSON_FILE)["4629"])

    #  master_json = cache.read_json(MASTER_JSON_FILE)
    #  trait_counts = rarity.getTraitCounts(master_json)
    #  #  pprint(trait_counts)
    #  #  pprint(rarity.calcRarestTraits(master_json, trait_counts))
    #  #  pprint(rarity.calcTraitScores(master_json, trait_counts))
    #  trait_scores = rarity.calcTraitScores(master_json, trait_counts)
    #  #  pprint(trait_scores)
    #  cache.cache_json(trait_scores, SCORES_FILE)


    #  pprint(rarity.calcTokenScore(trait_scores, 4997))
    #  pprint(rarity.calcAllTokenScores(trait_scores))
    #  cache.cache_json(
            #  rarity.calcAllTokenScores(trait_scores), RANKS_FILE)

    #  pprint(cache.createMasterJSONThreaded(contract, 0, 100, 3))
