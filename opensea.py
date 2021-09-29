import cache
import constants

from datetime import datetime
from dateutil import tz
import json
import pdb
from pprint import pprint
import requests
from sys import argv

EVENTS_API = "https://api.opensea.io/api/v1/events"
API_HEADERS = {"Accept": "application/json"}
#  EVENT_TYPE = "successful"
EVENT_TYPE = "created"
#  MAX_LIMIT = 300
MAX_LIMIT = 50
#  MAX_LIMIT = 5

SALES_DIR = f"{constants.CACHE_DIR}/sales"
MASTER_SALES_FILE = f"{SALES_DIR}/master-os-sales.json"
MASTER_SALES_SUMMARY_FILE = f"{SALES_DIR}/master-os-sales-summary.json"

# master sales keys
TIMESTAMP_KEY = "timestamp"
TOKEN_ID_KEY = "token_id"
ETH_KEY = "eth"

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

def addSaleSummary(master_sale_summaries, sale):
    #  master_sale_summaries[sale["id"]] = {
    master_sale_summaries[str(sale["id"])] = {
            TIMESTAMP_KEY: sale["transaction"]["timestamp"],
            TOKEN_ID_KEY: sale["asset"]["token_id"],
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
    for listing in listings:
        eth = getEth(listing["starting_price"])
        token_id = listing['asset']['token_id']
        rank = ranks[token_id]['rank']
        if (listing["auction_type"] == "dutch" and 
                eth <= constants.ETH_FILTER and
                rank <= constants.RANK_FILTER):
            filtered_listings[rank] = {
                    "token_id": token_id,
                    "eth": eth,
                    }
    return filtered_listings
    

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
            #  sale_summaries = updateMasterSaleSummaries(0)
        #  else:
            #  printAllSaleSummaries(getCachedSaleSummaries(), int(argv[1]))
    #  else:
        #  printAllSaleSummaries(getCachedSaleSummaries())

    # listings 
    # step 1
    cache.cache_json(getSalesData(0), constants.LISTINGS_FILE)

    # step 2
    listings = getEventsList(
            cache.read_json(f"{constants.CACHE_DIR}/listings.json"))
    pprint(getFilteredListings(listings))
