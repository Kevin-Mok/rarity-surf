from constants import CACHE_DIR, RAW_CACHE_DIR, MASTER_JSON_FILE
from web3_api import getTokenMetadata
from pprint import pprint

import json 
import os
from os.path import isfile, join, splitext

def cacheTokenMetadata(contract, startTokenNum, endTokenNum):
    for tokenNum in range(startTokenNum, endTokenNum + 1):
        tokenMetadata = getTokenMetadata(contract, tokenNum)
        with open(f"{RAW_CACHE_DIR}/{tokenNum}.json", 'w') as out:
            print(f"Caching Token #{tokenNum} to {out.name}:")
            pprint(tokenMetadata)
            json.dump(tokenMetadata, out, indent=2)

def getRawCacheFiles():
    return [file for file in os.listdir(RAW_CACHE_DIR) 
            if isfile(join(RAW_CACHE_DIR, file))]

def initMasterJSON():
    master_json = {}
    for file_name in getRawCacheFiles():
        with open(join(RAW_CACHE_DIR, file_name)) as json_file:
            master_json[file_name.removesuffix('.json')] = json.load(json_file)
    return master_json

#  def cacheMasterJSON(master_json):
    #  with open(MASTER_JSON_FILE, 'w') as out:
        #  json.dump(master_json, out, indent=2)

#  def readMasterJSON():
    #  with open(MASTER_JSON_FILE) as master_json:
        #  return json.load(master_json)

def cache_json(json_to_cache, file_name):
    with open(file_name, 'w') as out:
        json.dump(json_to_cache, out, indent=2)
        #  json.dump(json_to_cache, out)

def read_json(file_name):
    with open(file_name) as in_file:
        return json.load(in_file)

def updateMasterJSON(master_json, tokenNum, tokenData):
    pass
