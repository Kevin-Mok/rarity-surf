import cache
import constants
import web3_api

from pprint import pprint

IPFS_URL = "https://ipfs.io/ipfs"
OS_ASSETS_URL = "https://opensea.io/assets"
# 7s
MAX_SUPPLY = 7000
# uwucrew
#  MAX_SUPPLY = 9670

def initTraitTypes(master_json):
    trait_counts = {}
    attributes = master_json["1"]["attributes"]
    for attribute in attributes:
        trait_counts[attribute["trait_type"]] = {}
    return trait_counts

def incrTraitValue(trait_counts, attribute):
    if attribute["value"] in trait_counts[attribute["trait_type"]]:
        trait_counts[attribute["trait_type"]][attribute["value"]] += 1
    else:
        trait_counts[attribute["trait_type"]][attribute["value"]] = 1

def getTraitCounts(master_json):
    trait_counts = initTraitTypes(master_json)
    for token_json in master_json.values():
        #  pprint(token_json)
        for attribute in token_json["attributes"]:
            incrTraitValue(trait_counts, attribute)
    return trait_counts

def calcRarestTraits(master_json, trait_counts):
    trait_percentages = initTraitTypes(master_json)
    for trait_type in trait_counts:
        for trait in trait_counts[trait_type]:
            trait_percentages[trait_type][trait] = \
                    trait_counts[trait_type][trait] / MAX_SUPPLY
    return trait_percentages

def calcTraitScore(trait_count):
    return 1 / trait_count / MAX_SUPPLY * (10 ** 8)

def calcTraitScores(master_json, trait_counts):
    trait_scores = initTraitTypes(master_json)
    for trait_type in trait_counts:
        for trait in trait_counts[trait_type]:
            trait_scores[trait_type][trait] = \
                    calcTraitScore(trait_counts[trait_type][trait])
    return trait_scores

def calcTokenScore(trait_scores, token_num):
    token_file = f"{constants.RAW_CACHE_DIR}/{token_num}.json"
    token_json = cache.read_json(token_file)
    #  pprint(token_json)
    token_score = 0
    for attribute in token_json["attributes"]:
        #  pprint(attribute)
        token_score += \
                trait_scores[attribute["trait_type"]][attribute["value"]]
    return token_score

def formatPercentage(percentage):
    return f"{percentage * 100:.1f}%"

def getRarestAttributes(rarest_traits, attributes):
    attribute_rarities = []
    for attribute in attributes:
        rarity_percentage = rarest_traits[attribute["trait_type"]][attribute["value"]]
        attribute_rarities.append({
                "trait_type": attribute["trait_type"],
                "trait": attribute["value"],
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

    for i in range(MAX_SUPPLY):
        token_scores[i] = calcTokenScore(trait_scores, i)
    sorted_token_scores = sorted(
            token_scores.items(), key=lambda x: x[1], reverse=True)

    ranked_tokens = {}
    rank = 1
    for token_score in sorted_token_scores:
        token_id = str(token_score[0])
        rarest_token_traits = getRarestAttributes(rarest_traits,
                master_json[token_id]["attributes"])
        image_ipfs_hash = web3_api.getIPFSHash(
                master_json[token_id]["image"])
        os_url = f"{OS_ASSETS_URL}/{constants.CONTRACT_ADDRESS}/{token_id}", 
        ranked_tokens[rank] = {
                "id": token_id,
                "score": token_score[1],
                "rarest_traits": rarest_token_traits,
                "image_url": f"{IPFS_URL}/{image_ipfs_hash}",
                "os_url": os_url,
                }
        rank += 1
    return ranked_tokens
