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

MASTER_SALES_FILE = f"{constants.CACHE_DIR}/master-os-sales.json"

def getSalesData(offset):
    querystring = {
            "asset_contract_address": constants.SEVENS_CONTRACT_ADDRESS,
            "event_type": EVENT_TYPE,
            "offset": offset,
            "limit":"300"}
    api_request = requests.request("GET", EVENTS_API,
            headers=API_HEADERS, params=querystring)
    return json.loads(api_request.text)

def getSalesFileName(offset):
    return f"{constants.CACHE_DIR}/os-sales-{offset}.json"

def cacheSalesData(sales_data, offset):
    cache.cache_json(sales_data, getSalesFileName(offset))

def readSalesData(offset):
    with open(getSalesFileName(offset)) as sales_data:
        return json.load(sales_data)

def getEventsList(json):
    return json["asset_events"]

def getEth(eth):
    return float(f"{int(eth) * (10 ** -18):.2f}")
    #  return f"{int(eth) * (10 ** -18):.2f}"

def filterSales(sale_events, geThan):
    return [sale_event for sale_event in sale_events
            if getEth(sale_event["total_price"]) >= geThan]

def formatTimestamp(timestamp):
    # 2021-09-16T05:49:06
    datetime_obj = datetime.strptime(timestamp,
            '%Y-%m-%dT%H:%M:%S')\
            .replace(tzinfo=tz.tzutc())\
            .astimezone(tz.tzlocal())
    return datetime_obj.strftime('%d %H:%M')

def printAllSales(all_sale_events, geThan):
    all_sales = [all_sale_events[sale_id] 
            for sale_id in sorted(all_sale_events)
            if all_sale_events[sale_id]["transaction"] is not None]
    for sale in filterSales(all_sales, geThan):
        txn_time = formatTimestamp(sale["transaction"]["timestamp"])
        token_id = sale["asset"]["token_id"]
        #  sale_price = getEth(sale["total_price"])
        sale_price = str(getEth(sale["total_price"]))
        print(f"{txn_time} | #{token_id:4} = " + 
              #  f"{sale_price.rjust(4)} ETH")
              #  f"{sale_price:.2f} ETH")
              f"{sale_price:4} ETH")

def createMasterSaleEvents(max_offet):
    all_sale_events = {}
    for i in range(max_offet + 1):
        sale_events = getEventsList(readSalesData(i))
        for sale in sale_events:
            all_sale_events[sale["id"]] = sale
    return all_sale_events

if __name__ == "__main__":
    #  offset = 0
    #  cacheSalesData(getSalesData(offset), offset)
    #  TODO: create separate raw dirs for metadata/sales # 
    #  cache.cache_json(getSalesData(offset), getSalesFileName(offset))

    #  with open(getSalesFileName(10), 'w') as out:
        #  json.dump(sale_events[0], out, indent=2)
    #  for sale in filterSales(sale_events, 3):
        #  print(getSaleSummary(sale))

    #  all_sale_events = createMasterSaleEvents(1)
    #  pprint(all_sale_events[921818069])
    #  pprint(len(all_sale_events))
    #  for sale_id in all_sale_events:
        #  printSaleSummary(all_sale_events[sale_id])
    #  printAllSales(all_sale_events, 3)
    #  cache.cache_json(all_sale_events, MASTER_SALES_FILE)
    all_sale_events = cache.read_json(MASTER_SALES_FILE)
    #  print(len(all_sale_events))
    pprint(all_sale_events["914642515"])
