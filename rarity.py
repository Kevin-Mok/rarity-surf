import cache
import constants

from pprint import pprint

SEVENS_SUPPLY = 7000

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
                    trait_counts[trait_type][trait] / SEVENS_SUPPLY
    return trait_percentages

def calcTraitScores(master_json, trait_counts):
    trait_scores = initTraitTypes(master_json)
    for trait_type in trait_counts:
        for trait in trait_counts[trait_type]:
            trait_scores[trait_type][trait] = \
                    1 / trait_counts[trait_type][trait] / SEVENS_SUPPLY
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

def calcAllTokenScores(trait_scores):
    token_scores = {}
    for i in range(SEVENS_SUPPLY):
        #  print(f"#{i}: {calcTokenScore(trait_scores, i)}")
        token_scores[i] = calcTokenScore(trait_scores, i)
    sorted_token_scores = sorted(
            token_scores.items(), key=lambda x: x[1], reverse=True)

    ranked_tokens = {}
    rank = 1
    for token_score in sorted_token_scores:
        ranked_tokens[rank] = token_score[0]
        #  print(f"{rank}: #{token_num}")
        rank += 1
    return ranked_tokens
