import constants

from datetime import datetime
from dateutil import tz
import json
from pprint import pprint
import requests

EVENTS_API = "https://api.opensea.io/api/v1/events"
API_HEADERS = {"Accept": "application/json"}
EVENT_TYPE = "successful"

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
    with open(getSalesFileName(offset), 'w') as out:
        json.dump(sales_data, out, indent=2)

def readSalesData(offset):
    with open(getSalesFileName(offset)) as sales_data:
        return json.load(sales_data)

def getEventsList(json):
    return json["asset_events"]

def getEth(eth):
    return float(f"{int(eth) * (10 ** -18):.2f}")

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

def getSaleSummary(sale):
    txn_time = formatTimestamp(sale["transaction"]["timestamp"])
    token_id = sale["asset"]["token_id"]
    sale_price = getEth(sale["total_price"])
    return f"{txn_time} | #{token_id:4} = {sale_price} ETH"

if __name__ == "__main__":
    #  offset = 0
    #  cacheSalesData(getSalesData(offset), offset)

    sale_events = getEventsList(readSalesData(0))
    #  with open(getSalesFileName(10), 'w') as out:
        #  json.dump(sale_events[0], out, indent=2)
    #  pprint(filterSales(sale_events, 1))
    for sale in filterSales(sale_events, 3): 
        print(getSaleSummary(sale))
