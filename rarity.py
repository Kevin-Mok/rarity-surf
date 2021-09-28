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
