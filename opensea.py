import constants

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

if __name__ == "__main__":
    #  pass
    #  offset = 0
    #  cacheSalesData(getSalesData(offset), offset)

    # print created events
    #  event_data = readSalesData(1)
    #  event_types = {}
    #  for event in event_data["asset_events"]:
        #  event_types[event["event_type"]] = ''
    #  created_events = [event for event in event_data["asset_events"]
            #  if event["event_type"] == "created"]
    #  #  pprint(created_events)
    #  with open('created-events.json', 'w') as out:
        #  json.dump(created_events, out, indent=2)

    #  created price is event["starting_price"] # 

    # get specific token events
    #  token_id = 500
    #  querystring = {
            #  "asset_contract_address": constants.SEVENS_CONTRACT_ADDRESS,
            #  "token_id": token_id,}
    #  api_request = requests.request("GET", EVENTS_API,
            #  headers=API_HEADERS, params=querystring)
    #  cacheSalesData(json.loads(api_request.text), token_id)
    pprint(readSalesData(1))
