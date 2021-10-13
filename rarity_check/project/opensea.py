import project.cache as cache
import project.constants as constants
from project.get_obj import get_token_obj_os

from datetime import datetime
from dateutil import tz
from math import ceil
import json
import pdb
from pprint import pprint
import requests
from sys import argv

OS_API = "https://api.opensea.io/api/v1"
ASSETS_API = f"{OS_API}/assets"
EVENTS_API = f"{OS_API}/events"
API_HEADERS = {"Accept": "application/json"}

#  TODO: pass in as arg # 
#  EVENT_TYPE = "successful" # sales
#  MAX_LIMIT = 300
EVENT_TYPE = "created" # listings
MAX_LIMIT = 50
ASSETS_MAX_LIMIT = 30
#  ASSETS_MAX_LIMIT = 2
LISTINGS_MAX_LIMIT = 50

#  MAX_LIMIT = 5 # tesing

SALES_DIR = f"{constants.CACHE_DIR}/sales"
MASTER_SALES_FILE = f"{SALES_DIR}/master-os-sales.json"
MASTER_SALES_SUMMARY_FILE = f"{SALES_DIR}/master-os-sales-summary.json"

DETAIL_KEY = "detail"
THROTTLED_MSG = "Request was throttled."
TIMESTAMP_KEY = "timestamp"
ETH_KEY = "eth"

#  def getAssetsAPI(token_id_list):
def getAssetsAPI(offset):
    querystring = {
            #  "asset_contract_address": constants.CONTRACT_ADDRESS,
            #  "token_ids": token_id_list,
            "collection": "bitznft",
            "offset": offset,
            #  "order_by": "listing_date",
            "limit": ASSETS_MAX_LIMIT}
    api_request = requests.request("GET", ASSETS_API,
            headers=API_HEADERS, params=querystring)
    #  pprint(api_request)
    return json.loads(api_request.text)["assets"]

def getSalesData(page):
    print(f"Fetching page {page} of events.")
    querystring = {
            "asset_contract_address": constants.CONTRACT_ADDRESS,
            "event_type": EVENT_TYPE,
            "offset": page * MAX_LIMIT,
            #  "auction_type": "dutch",
            "limit": MAX_LIMIT}
    api_request = requests.request("GET", EVENTS_API,
            headers=API_HEADERS, params=querystring)
    #  pprint(api_request)
    return json.loads(api_request.text)

def getEventsList(json):
    return json["asset_events"]

def getEth(eth):
    return float(f"{int(eth) * (10 ** -18):.2f}")
    #  return f"{int(eth) * (10 ** -18):.2f}"

def filterSaleSummariesByPrice(sale_summaries, geThan):
    return [sale_summaries[sale_id] for sale_id in sale_summaries
            if sale_summaries[sale_id][ETH_KEY] >= geThan]

def formatTimestamp(timestamp):
    # 2021-09-16T05:49:06
    datetime_obj = datetime.strptime(timestamp,
            '%Y-%m-%dT%H:%M:%S')\
            .replace(tzinfo=tz.tzutc())\
            .astimezone(tz.tzlocal())
    return datetime_obj.strftime('%d %H:%M')

#  def filterInvalidSales(all_sale_events):
    #  return [all_sale_events[sale_id]
            #  for sale_id in sorted(all_sale_events)
            #  if all_sale_events[sale_id]["transaction"] is not None
            #  and all_sale_events[sale_id]["asset"] is not None]

def printAllSaleSummaries(all_sale_summaries, geThan=0):
    for sale in filterSaleSummariesByPrice(
            all_sale_summaries, geThan):
        print(f"{formatTimestamp(sale[TIMESTAMP_KEY])} | " +
              f"#{sale[TOKEN_ID_KEY]:4} = " + 
              f"{sale[ETH_KEY]:4} ETH")

def getTokenIDFromObj(obj):
    return obj["asset"]["token_id"]

def addSaleSummary(master_sale_summaries, sale):
    master_sale_summaries[str(sale["id"])] = {
            TIMESTAMP_KEY: sale["transaction"]["timestamp"],
            #  TOKEN_ID_KEY: sale["asset"]["token_id"],
            TOKEN_ID_KEY: getTokenIDFromObj(sale),
            ETH_KEY: getEth(sale["total_price"])
            }
    return master_sale_summaries

def updateMasterSaleSummaries(max_page):
    master_sale_summaries = cache.read_json(
            MASTER_SALES_SUMMARY_FILE)
    starting_sale_summaries = len(master_sale_summaries)
    print(f"Starting: {starting_sale_summaries}")
    for i in range(max_page + 1):
        new_sales = getEventsList(getSalesData(i))
        for sale in new_sales:
            master_sale_summaries = addSaleSummary(
                    master_sale_summaries, sale)
    added_sale_summaries = len(master_sale_summaries) -\
            starting_sale_summaries
    print(f"Added: {added_sale_summaries}")
    print(f"Final: {len(master_sale_summaries)}")
    cache.cache_json(master_sale_summaries,
            MASTER_SALES_SUMMARY_FILE)
    return master_sale_summaries

def getCachedSaleSummaries():
    return cache.read_json(MASTER_SALES_SUMMARY_FILE)

def getFilteredListings(listings):
    ranks = cache.read_json(constants.RANKS_FILE)
    filtered_listings = {}
    for listing in listings.values():
        eth = getEth(listing["starting_price"])
        if listing['asset']:
            token_id = listing['asset']['token_id']
            #  if (token_id not in filtered_listings and
                    #  token_id in ranks):
            if token_id in ranks:
                rank = ranks[token_id]['rank']
                if (listing["auction_type"] == "dutch" and 
                        eth <= constants.ETH_FILTER and
                        rank <= constants.RANK_FILTER):
                    filtered_listings[token_id] = {
                            constants.RANK_KEY: rank,
                            ETH_KEY: eth,
                            }
    #  pprint(filtered_listings)
    return filtered_listings

def getAllAssets(token_ids):
    master_assets = []
    for i in range(0, len(token_ids), ASSETS_MAX_LIMIT):
        master_assets += getAssetsAPI(token_ids[i:i + ASSETS_MAX_LIMIT])
    return master_assets

def inputAllAssets(project):
    for offset in range(0, project.max_supply, ASSETS_MAX_LIMIT):
        for asset in getAssetsAPI(offset):
            token_obj = get_token_obj_os(project, asset)
            print(f"{token_obj} Traits:")
            print(token_obj.traits.all())

def checkIfStillListed(listings):
    assets = getAllAssets(list(listings.keys()))
    cache.cache_json(assets, constants.ASSETS_FILE)
    listed_assets = []
    for asset in assets:
        if asset["sell_orders"]:
            raw_cur_price = asset["sell_orders"][0]["current_price"]
            cur_price = getEth(raw_cur_price.split(".", 1)[0])
            if cur_price <= constants.ETH_FILTER:
                listings[asset["token_id"]][ETH_KEY] = cur_price
                listed_assets.append(asset["token_id"])
    return {token_id:values 
            for (token_id, values) in listings.items()
            if token_id in listed_assets}

def sortListingsByRank(listings):
    ranked_listings = {}
    for (token_id, values) in listings.items():
        ranked_listings[values[constants.RANK_KEY]] = {
                TOKEN_ID_KEY: token_id,
                ETH_KEY: values[ETH_KEY],
                }
    return ranked_listings

def createMasterListings(pages):
    master_listings = {}
    for page in range(pages):
        page_listings = getEventsList(getSalesData(page))
        for listing in page_listings:
            master_listings[listing["id"]] = listing
            #  TODO: create simplified updatable listing per token
            #  master_listings[getTokenIDFromObj(listing)] = {
                    #  ETH_KEY: ,
                    #  TIMESTAMP_KEY: ,
                    #  }
    return master_listings

def updateMasterListings(start_page, end_page):
    master_listings = cache.read_json(constants.LISTINGS_FILE)
    print(f"Starting listings: {len(master_listings)}")
    for page in range(start_page, end_page + 1):
        page_listings = getEventsList(getSalesData(page))
        for listing in page_listings:
            master_listings[str(listing["id"])] = listing
    print(f"Ending listings: {len(master_listings)}")
    cache.cache_json(master_listings, constants.LISTINGS_FILE)
    return master_listings

def getRefilteredListings():
    listings = cache.read_json(constants.LISTINGS_FILE)
    filtered_listings = getFilteredListings(listings)
    filtered_listings = checkIfStillListed(filtered_listings)
    ranks = cache.read_json(constants.RANKS_FILE)

    filtered_listings_info = {}
    for token_id in filtered_listings.keys():
        rank = filtered_listings[token_id][constants.RANK_KEY]
        filtered_listings_info[rank] = (filtered_listings[token_id] |
                ranks[token_id])
        filtered_listings_info[rank][constants.TOKEN_ID_KEY] = token_id
    return filtered_listings_info

if __name__ == "__main__":
    # sales
    """
    options for argv[1]:
    - "update"
    - ETH to filter by
    - none to print all
    """
    #  if len(argv) > 1:
        #  if argv[1] == "update":
            #  sale_summaries = updateMasterSaleSummaries(1)
        #  else:
            #  printAllSaleSummaries(getCachedSaleSummaries(), float(argv[1]))
    #  else:
        #  printAllSaleSummaries(getCachedSaleSummaries())

    #  updateMasterListings(pages)
    #  updateMasterListings(0, 1)
    #  pages = ceil(constants.TOTAL_LISTED / MAX_LIMIT)

    # step 1: create initial listings
    cache.cache_json(createMasterListings(
        #  constants.TOTAL_LISTED * 2 // LISTINGS_MAX_LIMIT),
        constants.TOTAL_LISTED // LISTINGS_MAX_LIMIT),
        constants.LISTINGS_FILE)

    # step 2: filter listings
    cache.cache_json(getRefilteredListings(), constants.FILTERED_LISTINGS_FILE)
