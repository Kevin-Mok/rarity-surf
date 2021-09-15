import constants

import json
from pprint import pprint
import requests

EVENTS_API = "https://api.opensea.io/api/v1/events"
API_HEADERS = {"Accept": "application/json"}

def getSalesData():
    querystring = {
            "asset_contract_address": constants.SEVENS_CONTRACT_ADDRESS,
            #  "event_type":"sales",
            "only_opensea":"false",
            "offset":"0",
            "limit":"100"}
    api_request = requests.request("GET", EVENTS_API,
            headers=API_HEADERS, params=querystring)
    return json.loads(api_request.text)
    

if __name__ == "__main__":
    #  pprint(getSalesData()["asset_events"])
    #  with open('os-sales.json', 'w') as out:
        #  json.dump(getSalesData(), out, indent=2)
    with open('os-sales.json') as sales_data_raw:
        sales_data = json.load(sales_data_raw)
        pprint(sales_data["asset_events"])
