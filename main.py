import cache
import constants
import rarity

from pprint import pprint
from web3_api import getContract, getTokenMetadata

if __name__ == "__main__":
    #  contract = getContract()
    #  cache.cacheTokenMetadata(contract, 1000, 1001)
    #  pprint(cache.createMasterJSON(contract, 1, 50))
    #  cache.cacheTokenMetadataThreaded(0, 100, 50)
    #  cache.cacheTokenMetadataThreaded(0, 10, 5)
    #  pprint(getTokenMetadata(123))

    #  pprint(cache.initMasterJSON())
    #  TODO: test new general cache fxns # 
    #  cache.cacheMasterJSON(cache.initMasterJSON())
    #  cache.cache_json(cache.initMasterJSON(), MASTER_JSON_FILE)
    #  pprint(cache.read_json(MASTER_JSON_FILE)["4629"])

    master_json = cache.read_json(constants.MASTER_JSON_FILE)
    #  pprint(master_json["1353"])
    #  trait_counts = rarity.getTraitCounts(master_json)
    #  rarest_traits = rarity.calcRarestTraits(master_json,
            #  trait_counts)
    #  cache.cache_json(rarest_traits,
            #  constants.RARE_TRAITS_FILE)
    #  trait_scores = rarity.calcTraitScores(master_json, trait_counts)

    #  cache.cache_json(trait_scores, SCORES_FILE)

    #  pprint(rarity.calcTokenScore(trait_scores, 4997))
    #  pprint(rarity.calcAllTokenScores(trait_scores))
    #  cache.cache_json(
            #  rarity.calcAllTokenScores(master_json,
                #  trait_scores, rarest_traits), RANKS_FILE)
    cache.cache_json(
            rarity.calcAllTokenScores(master_json),
            constants.RANKS_FILE)
    #  rarity.getRarestAttributes(rarest_traits,
            #  master_json["0"]["attributes"])

    #  pprint(cache.createMasterJSONThreaded(contract, 0, 100, 3))
