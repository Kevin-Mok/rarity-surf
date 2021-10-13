import project.cache as cache
import project.constants as constants
import project.get_obj as get_obj
from .models import Project, TraitType, TraitValue, Token
import project.web3_api as web3_api

from pprint import pprint
from statistics import mean

IPFS_URL = "https://ipfs.io/ipfs"
OS_ASSETS_URL = "https://opensea.io/assets"

DISCREPANCY_KEY = "discrepancy"
DISCREPANCY_PERCENTAGE_KEY = "discrepancy_percentage"
NO_TRAIT_KEY = "no_trait"
NUMBER_TRAITS_KEY = "number_traits"
TOOLS_RANK_KEY = "tools_rank"
#  TRAIT_TYPE_KEY = "trait_type"
#  TRAIT_VALUE_KEY = "value"

def checkNothingTrait(trait_value):
    return (str(trait_value).startswith("No ") or
            trait_value == "Nothing")

def addNumberTraits(master_json):
    for token_json in master_json.values():
        #  attributes = token_json[constants.ATTRIBUTES_KEY]
        attributes = [attribute 
                for attribute in token_json[constants.ATTRIBUTES_KEY]
                if attribute[constants.TRAIT_TYPE_KEY] 
                not in constants.IGNORED_TRAIT_TYPES]
        num_traits = len(attributes)
        no_traits = [attribute[constants.TRAIT_VALUE_KEY]
                for attribute in attributes
                if checkNothingTrait(attribute[constants.TRAIT_VALUE_KEY])]
        num_traits -= len(no_traits)
        number_traits_attribute = {
                constants.TRAIT_TYPE_KEY: NUMBER_TRAITS_KEY,
                constants.TRAIT_VALUE_KEY: num_traits,
                }
        token_json[constants.ATTRIBUTES_KEY].append(number_traits_attribute)

def initTraitTypes(master_json):
    trait_counts = { NUMBER_TRAITS_KEY: {} }
    for token_json in master_json.values():
        attributes_to_add = [traits[constants.TRAIT_TYPE_KEY] 
                for traits in token_json[constants.ATTRIBUTES_KEY]
                if traits[constants.TRAIT_TYPE_KEY] not in trait_counts]
        for attribute in attributes_to_add:
            trait_counts[attribute] = {}
    return trait_counts

def incrTraitValue(trait_counts, trait_type, trait_value):
    if trait_value in trait_counts[trait_type]:
        trait_counts[trait_type][trait_value] += 1
    else:
        trait_counts[trait_type][trait_value] = 1

def getEquivalentTrait(trait_value):
    if trait_value == "No Aura Plain":
        return "No Aura"
    return trait_value

def getTraitCounts(master_json):
    trait_counts = initTraitTypes(master_json)
    for token_json in master_json.values():
        token_attributes = {}
        for attribute in token_json[constants.ATTRIBUTES_KEY]:
            token_attributes[attribute[constants.TRAIT_TYPE_KEY]] = \
                    attribute[constants.TRAIT_VALUE_KEY]

        for trait_type in trait_counts:
            trait_value_incr = getEquivalentTrait(
                    token_attributes[trait_type]
                    if trait_type in token_attributes
                    else NO_TRAIT_KEY)
            incrTraitValue(trait_counts, trait_type, trait_value_incr)
    return trait_counts

def addTraitValueStats(project):
    for trait_type_obj in project.traittype_set.all():
        all_trait_values = trait_type_obj.traitvalue_set.all()
        for trait_value_obj in all_trait_values:
            trait_value_obj.count = trait_value_obj.token_set.count()
            trait_value_obj.rarity = round(trait_value_obj.count /
                    project.max_supply * 100, 2)

            base_score_multiplier = 4 / 5
            trait_value_obj.score = round(
                    1 / trait_value_obj.count / project.max_supply /
                    len(all_trait_values) * (10 ** 9) * base_score_multiplier, 2)

            trait_value_obj.save()
            print(f"Set {trait_value_obj} count, rarity and score.")

def calcRarestTraits(master_json, trait_counts):
    trait_percentages = initTraitTypes(master_json)
    for trait_type in trait_counts:
        for trait in trait_counts[trait_type]:
            trait_percentages[trait_type][trait] = \
                    trait_counts[trait_type][trait] / constants.MAX_SUPPLY
    return trait_percentages

def calcTraitScore(trait_count, num_trait_values):
    # from rarity.tools article + trait normalization
    # https://raritytools.medium.com/ranking-rarity-understanding-rarity-calculation-methods-86ceaeb9b98c
    base_score_multiplier = 3 / 5
    base_score = round(1 / trait_count / constants.MAX_SUPPLY /
            num_trait_values * (10 ** 9) * base_score_multiplier, 2)
    return base_score

def calcTraitScores(master_json, trait_counts):
    trait_scores = initTraitTypes(master_json)
    for trait_type in trait_counts:
        for trait in trait_counts[trait_type]:
            trait_scores[trait_type][trait] = \
                    calcTraitScore(trait_counts[trait_type][trait],
                            len(trait_counts[trait_type]))
    return trait_scores

def calcTokenScore(master_json, trait_scores, token_num):
    token_score = 0
    for attribute in master_json[token_num][constants.ATTRIBUTES_KEY]:
        if (attribute[constants.TRAIT_TYPE_KEY]
                not in constants.IGNORED_TRAIT_TYPES):
            trait_value = getEquivalentTrait(attribute[constants.TRAIT_VALUE_KEY])
            token_score += \
                    trait_scores[attribute[constants.TRAIT_TYPE_KEY]][trait_value]
    return token_score

def addTokenScores(project):
    for token_obj in Token.objects.all():
        token_obj.score = sum([trait_value_obj.score 
            for trait_value_obj in token_obj.traits.all()])
        token_obj.save()
        print(f"Set {token_obj} score to {token_obj.score}.")

def addTokenURLs(project):
    for token_obj in Token.objects.all():
        token_obj.os_url = f"{OS_ASSETS_URL}/" + \
                f"{project.contract_address}/" + \
                f"{token_obj.number}/"
        token_obj.save()
        print(f"Set {token_obj} URL to {token_obj.os_url}.")

def formatPercentage(percentage):
    return f"{percentage * 100:.2f}%"

def getRarestAttributes(rarest_traits, attributes):
    attribute_rarities = []
    for attribute in attributes:
        trait_value = getEquivalentTrait(attribute[constants.TRAIT_VALUE_KEY])
        rarity_percentage = rarest_traits[
                attribute[constants.TRAIT_TYPE_KEY]][trait_value]
        attribute_rarities.append({
                constants.TRAIT_TYPE_KEY: attribute[constants.TRAIT_TYPE_KEY],
                "trait": trait_value,
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

def interactiveRankSearch():
    ranks = cache.read_json(constants.RANKS_FILE)
    while True:
        token_id = input('Token #: ')
        if token_id in ranks:
            pprint(ranks[token_id])
        else:
            print("Token # not found.")

def getAllDiscrepanciesDict():
    """Compare own ranks with rarity.tools ranks.
    """
    my_ranks = cache.read_json(constants.RANKS_FILE)
    tools_ranks = convertToolsRanks()
    discrepancies = {}
    #  for token_id in range(constants.MAX_SUPPLY):
    for token_id in range(1, constants.MAX_SUPPLY + 1):
        token_id_str = str(token_id)
        my_rank = int(my_ranks[token_id_str][constants.RANK_KEY])
        tools_rank = int(tools_ranks[token_id_str])
        discrepancy = abs(my_rank - tools_rank)
        discrepancies[token_id] = {
                "my_rank": my_rank,
                TOOLS_RANK_KEY: tools_rank,
                DISCREPANCY_KEY: discrepancy,
                DISCREPANCY_PERCENTAGE_KEY: discrepancy / tools_rank,
                }
    return discrepancies

def getAvgDiscrepancies(max_rank=constants.MAX_SUPPLY):
    # initialize values
    all_discrepancies_dicts = getAllDiscrepanciesDict().values()
    all_discrepancies = []
    all_discrepancy_percentages = []
    # filter discrepancies_dicts under max_rank
    filtered_discrepancies_dicts = [discrepancy_dict 
            for discrepancy_dict in all_discrepancies_dicts
            if discrepancy_dict[TOOLS_RANK_KEY] <= max_rank]
    # add values to dicts
    for discrepancy_dict in filtered_discrepancies_dicts:
        all_discrepancies.append(discrepancy_dict[DISCREPANCY_KEY])
        all_discrepancy_percentages.append(
                discrepancy_dict[DISCREPANCY_PERCENTAGE_KEY])
    avg_discrepancy_percentage = mean(all_discrepancy_percentages) * 100
    print(f"Avg. Discrepancy: {mean(all_discrepancies)}")
    print(f"Avg. Discrepancy %: {avg_discrepancy_percentage:2f}")

def convertToolsRanks():
    """Convert rarity.tools ranks to by token ID.
    """
    tools_ranks = cache.read_json(constants.TOOLS_RANKS_FILE)
    return {token_id.lstrip("0"): rank for (rank, token_id) 
            in tools_ranks.items()}
    
if __name__ == "__main__":
    #  interactiveRankSearch()
    #  getAvgDiscrepancies(250)
    getAvgDiscrepancies()
    #  pprint(getAllDiscrepanciesDict())
