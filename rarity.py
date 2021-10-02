import cache
import constants
import web3_api

from pprint import pprint

IPFS_URL = "https://ipfs.io/ipfs"
OS_ASSETS_URL = "https://opensea.io/assets"

NO_TRAIT_KEY = "no_trait"
TRAIT_TYPE_KEY = "trait_type"
TRAIT_VALUE_KEY = "value"

def initTraitTypes(master_json):
    trait_counts = {}
    for token_json in master_json.values():
        attributes_to_add = [traits[TRAIT_TYPE_KEY] 
                for traits in token_json[constants.ATTRIBUTES_KEY]
                if traits[TRAIT_TYPE_KEY] not in trait_counts]
        for attribute in attributes_to_add:
            trait_counts[attribute] = {}
    return trait_counts

def incrTraitValue(trait_counts, trait_type, trait_value):
    if trait_value in trait_counts[trait_type]:
        trait_counts[trait_type][trait_value] += 1
    else:
        trait_counts[trait_type][trait_value] = 1

def getTraitCounts(master_json):
    trait_counts = initTraitTypes(master_json)
    for token_json in master_json.values():
        token_attributes = {}
        for attribute in token_json[constants.ATTRIBUTES_KEY]:
            token_attributes[attribute[TRAIT_TYPE_KEY]] = \
                    attribute[TRAIT_VALUE_KEY]

        for trait_type in trait_counts:
            trait_value_incr = (token_attributes[trait_type]
                    if trait_type in token_attributes
                    else NO_TRAIT_KEY)
            incrTraitValue(trait_counts, trait_type, trait_value_incr)
    return trait_counts

def calcRarestTraits(master_json, trait_counts):
    trait_percentages = initTraitTypes(master_json)
    for trait_type in trait_counts:
        for trait in trait_counts[trait_type]:
            trait_percentages[trait_type][trait] = \
                    trait_counts[trait_type][trait] / constants.MAX_SUPPLY
    return trait_percentages

def calcTraitScore(trait_count):
    return 1 / trait_count / constants.MAX_SUPPLY * (10 ** 8)

def calcTraitScores(master_json, trait_counts):
    trait_scores = initTraitTypes(master_json)
    for trait_type in trait_counts:
        for trait in trait_counts[trait_type]:
            trait_scores[trait_type][trait] = \
                    calcTraitScore(trait_counts[trait_type][trait])
    return trait_scores

def calcTokenScore(master_json, trait_scores, token_num):
    token_score = 0
    for attribute in master_json[token_num][constants.ATTRIBUTES_KEY]:
        token_score += \
                trait_scores[attribute[TRAIT_TYPE_KEY]][attribute[TRAIT_VALUE_KEY]]
    return token_score

def formatPercentage(percentage):
    return f"{percentage * 100:.1f}%"

def getRarestAttributes(rarest_traits, attributes):
    attribute_rarities = []
    for attribute in attributes:
        rarity_percentage = rarest_traits[attribute[TRAIT_TYPE_KEY]][attribute[TRAIT_VALUE_KEY]]
        attribute_rarities.append({
                TRAIT_TYPE_KEY: attribute[TRAIT_TYPE_KEY],
                "trait": attribute[TRAIT_VALUE_KEY],
                "rarity": rarity_percentage,
                })

    sorted_attribute_rarities = sorted(attribute_rarities,
            key=lambda x: x["rarity"])
    for attribute in sorted_attribute_rarities:
        attribute["rarity"] = formatPercentage(attribute["rarity"])
    return sorted_attribute_rarities[:3]

def calcAllTokenScores(master_json):
    trait_counts = getTraitCounts(master_json)
    rarest_traits = calcRarestTraits(master_json, trait_counts)
    trait_scores = calcTraitScores(master_json, trait_counts)
    token_scores = {}

    for token_id in master_json.keys():
        token_scores[token_id] = calcTokenScore(master_json,
                trait_scores, token_id)
    sorted_token_scores = sorted(
            token_scores.items(), key=lambda x: x[1], reverse=True)

    ranked_tokens = {}
    rank = 1
    for token_score in sorted_token_scores:
        token_id = str(token_score[0])
        rarest_token_traits = getRarestAttributes(rarest_traits,
                master_json[token_id][constants.ATTRIBUTES_KEY])
        image_ipfs_hash = web3_api.getIPFSHash(
                master_json[token_id]["image"])
        os_url = f"{OS_ASSETS_URL}/{constants.CONTRACT_ADDRESS}/{token_id}", 
        ranked_tokens[token_id] = {
                constants.RANK_KEY: rank,
                "score": token_score[1],
                "rarest_traits": rarest_token_traits,
                "image_url": f"{IPFS_URL}/{image_ipfs_hash}",
                "os_url": os_url,
                }
        rank += 1
    return ranked_tokens

def getSortedRanks(ranks):
    ranks_list = []
    for token_id in ranks.keys():
        rank = ranks[token_id]
        rank[constants.TOKEN_ID_KEY] = token_id
        ranks_list.append(rank)
    sorted_ranks = sorted(ranks_list, key=lambda x: x[constants.RANK_KEY])
    return sorted_ranks

if __name__ == "__main__":
    master_json = cache.initMasterJSON()
    #  pprint(initTraitTypes(master_json))
    #  pprint(getTraitCounts(master_json))
