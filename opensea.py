import cache
import constants

from datetime import datetime
from dateutil import tz
import json
import pdb
from pprint import pprint
import requests

EVENTS_API = "https://api.opensea.io/api/v1/events"
API_HEADERS = {"Accept": "application/json"}
EVENT_TYPE = "successful"
MAX_LIMIT = 300

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
            "asset_contract_address": constants.SEVENS_CONTRACT_ADDRESS,
            "event_type": EVENT_TYPE,
            "offset": page * MAX_LIMIT,
            "limit": MAX_LIMIT}
    api_request = requests.request("GET", EVENTS_API,
            headers=API_HEADERS, params=querystring)
    return json.loads(api_request.text)

def getSalesFileName(page):
    return f"{SALES_DIR}/os-sales-{page}.json"

def cacheSalesData(page):
    cache.cache_json(getSalesData(page),
            getSalesFileName(page))

def readSalesData(page):
    return cache.read_json(getSalesFileName(page))
    #  with open(getSalesFileName(page)) as sales_data:
        #  return json.load(sales_data)

def getEventsList(json):
    return json["asset_events"]

def getEth(eth):
    return float(f"{int(eth) * (10 ** -18):.2f}")
    #  return f"{int(eth) * (10 ** -18):.2f}"

def filterSalesByPrice(sale_events, geThan):
    return [sale_event for sale_event in sale_events
            if getEth(sale_event["total_price"]) >= geThan]

def formatTimestamp(timestamp):
    # 2021-09-16T05:49:06
    datetime_obj = datetime.strptime(timestamp,
            '%Y-%m-%dT%H:%M:%S')\
            .replace(tzinfo=tz.tzutc())\
            .astimezone(tz.tzlocal())
    return datetime_obj.strftime('%d %H:%M')

def filterInvalidSales(all_sale_events):
    return [all_sale_events[sale_id] 
            for sale_id in sorted(all_sale_events)
            if all_sale_events[sale_id]["transaction"] is not None
            and all_sale_events[sale_id]["asset"] is not None]

def printAllSales(all_sale_events, geThan):
    #  all_sales = [all_sale_events[sale_id]
            #  for sale_id in sorted(all_sale_events)
            #  if all_sale_events[sale_id]["transaction"] is not None
            #  and all_sale_events[sale_id]["asset"] is not None]
    all_sales = filterInvalidSales(all_sale_events)
    for sale in filterSalesByPrice(all_sales, geThan):
        txn_time = formatTimestamp(sale["transaction"]["timestamp"])
        token_id = sale["asset"]["token_id"]
        sale_price = str(getEth(sale["total_price"]))
        print(f"{txn_time} | #{token_id:4} = " + 
              f"{sale_price:4} ETH")

def convertMasterSales():
    all_sales = cache.read_json(MASTER_SALES_FILE)
    all_valid_sales = filterInvalidSales(all_sales)
    master_sales_summary = {}
    for sale in all_valid_sales:
        master_sales_summary[sale["id"]] = {
                TIMESTAMP_KEY: sale["transaction"]["timestamp"],
                TOKEN_ID_KEY: sale["asset"]["token_id"],
                ETH_KEY: getEth(sale["total_price"])
                }
    return master_sales_summary

def createMasterSaleEvents(max_page):
    all_sale_events = {}
    for i in range(max_page + 1):
        sale_events = getEventsList(readSalesData(i))
        for sale in sale_events:
            all_sale_events[sale["id"]] = sale
    return all_sale_events

def updateMasterSaleEvents(max_page):
    all_sale_events = cache.read_json(MASTER_SALES_FILE)
    print(f"Starting master sales: {len(all_sale_events)}")
    for i in range(max_page + 1):
        new_sales = getEventsList(getSalesData(i))
        for sale in new_sales:
            all_sale_events[sale["id"]] = sale
    print(f"Ending master sales: {len(all_sale_events)}")
    cache.cache_json(all_sale_events, MASTER_SALES_FILE)
    return all_sale_events

if __name__ == "__main__":
    #  TODO: create separate raw dirs for metadata/sales # 
    #  for i in range(11, 15):
        #  cacheSalesData(i)
    #  cacheSalesData(0)

    #  TODO: only save/store summary data # 
    #  all_sale_events = createMasterSaleEvents(14)
    #  pprint(len(all_sale_events))
    #  cache.cache_json(all_sale_events, MASTER_SALES_FILE)

    #  TODO: add new data to existing # 
    #  TODO: write ETH limit sales to file # 
    #  all_sale_events = cache.read_json(MASTER_SALES_FILE)
    #  all_sale_events = updateMasterSaleEvents(1)
    #  print(len(all_sale_events))
    #  printAllSales(all_sale_events, 7)
    #  pprint(all_sale_events["914642515"])

    #  pprint(convertMasterSales())
    #  cache.cache_json(convertMasterSales(),
            #  MASTER_SALES_SUMMARY_FILE)
    cache.cache_json(cache.read_json(MASTER_SALES_SUMMARY_FILE),
            MASTER_SALES_SUMMARY_FILE)
