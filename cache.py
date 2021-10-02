from constants import CACHE_DIR, RAW_CACHE_DIR, MASTER_JSON_FILE
from web3_api import getTokenMetadata

import json 
from math import floor
import os
from os.path import isfile, join, splitext
from pprint import pprint
import threading

#  def cacheTokenMetadata(contract, startTokenNum, endTokenNum):
def cacheTokenMetadata(startTokenNum, endTokenNum):
    for tokenNum in range(startTokenNum, endTokenNum + 1):
        #  tokenMetadata = getTokenMetadata(contract, tokenNum)
        tokenMetadata = getTokenMetadata(tokenNum)
        with open(f"{RAW_CACHE_DIR}/{tokenNum}.json", 'w') as out:
            print(f"Caching Token #{tokenNum} to {out.name}:")
            #  pprint(tokenMetadata)
            json.dump(tokenMetadata, out, indent=2)

def cacheTokenMetadataThreadedHelper(cached_tokens, startTokenNum, endTokenNum, threadNum):
    for tokenNum in range(startTokenNum, endTokenNum + 1):
        if str(tokenNum) not in cached_tokens:
            tokenMetadata = getTokenMetadata(tokenNum)
            #  print(f"Thread #{threadNum}: Checking token #{tokenNum} for attributes.")
            if constants.ATTRIBUTES_KEY in tokenMetadata:
                with open(f"{RAW_CACHE_DIR}/{tokenNum}.json", 'w') as out:
                    print(f"Thread #{threadNum}: Caching Token #{tokenNum} to {out.name}.")
                    json.dump(tokenMetadata, out, indent=2)

def cacheTokenMetadataThreaded(startTokenNum, endTokenNum, threads):
    #  print(startTokenNum, endTokenNum, threads)
    cached_tokens = getCachedTokens()
    step = floor((endTokenNum - startTokenNum) / threads)
    threadStartTokenNum = startTokenNum
    for i in range(threads):
        threading.Thread(target=cacheTokenMetadataThreadedHelper,
                args=(cached_tokens,
                    threadStartTokenNum,
                    threadStartTokenNum + step, i)).start()
        threadStartTokenNum += step + 1

def getRawCacheFiles():
    return [file for file in os.listdir(RAW_CACHE_DIR) 
            if isfile(join(RAW_CACHE_DIR, file))]

def getCachedTokens():
    return [stripJSONSuffix(file) for file in getRawCacheFiles()]

def createMasterJSON(contract, startTokenNum, endTokenNum):
    master_json = {}
    for tokenNum in range(startTokenNum, endTokenNum + 1):
        tokenMetadata = getTokenMetadata(contract, tokenNum)
        print(f"Adding Token #{tokenNum} metadata to master JSON.")
        master_json[tokenNum] = tokenMetadata
    return master_json

def addTokensToMasterJSON(contract, master_json, startTokenNum,
        endTokenNum):
    for tokenNum in range(startTokenNum, endTokenNum + 1):
        tokenMetadata = getTokenMetadata(contract, tokenNum)
        print(f"Adding Token #{tokenNum} metadata to master JSON.")
        master_json[tokenNum] = tokenMetadata

def addTokensToMasterJSONThreaded(contract, master_json, startTokenNum,
        endTokenNum, threadNum):
    for tokenNum in range(startTokenNum, endTokenNum + 1):
        tokenMetadata = getTokenMetadata(contract, tokenNum)
        print(f"Thread #{threadNum}: Adding Token #{tokenNum} metadata to master JSON.")
        master_json[tokenNum] = tokenMetadata

def threadStepTest(threadNum, startTokenNum, endTokenNum):
    print(f"Thread #{threadNum}: {startTokenNum}-{endTokenNum}")

def createMasterJSONThreaded(contract, startTokenNum,
        endTokenNum, threads):
    master_json = {}
    step = floor((endTokenNum - startTokenNum) / threads)
    threadStartTokenNum = startTokenNum
    #  for i in range(startTokenNum, endTokenNum, step):
    for i in range(threads):
        #  thread.start_new_thread(addTokensToMasterJSON,
                #  (contract, master_json, startTokenNum, endTokenNum))
        #  threading.Thread(target=threadStepTest,
                #  args=(i, threadStartTokenNum,
                    #  threadStartTokenNum + step)).start()
        threading.Thread(target=addTokensToMasterJSONThreaded,
                args=(contract, master_json,
                    threadStartTokenNum,
                    threadStartTokenNum + step, i)).start()
        threadStartTokenNum += step + 1
    #  addTokensToMasterJSON(contract, startTokenNum, endTokenNum)
    return master_json

def stripJSONSuffix(file_name):
    return file_name.removesuffix('.json')

def initMasterJSON():
    master_json = {}
    for file_name in getRawCacheFiles():
        with open(join(RAW_CACHE_DIR, file_name)) as json_file:
            #  master_json[file_name.removesuffix('.json')] = json.load(json_file)
            master_json[stripJSONSuffix(file_name)] = json.load(json_file)
    return master_json

def cache_json(json_to_cache, file_name):
    with open(file_name, 'w') as out:
        print(f"Caching {file_name}.")
        json.dump(json_to_cache, out, indent=2, sort_keys=True)

def read_json(file_name):
    with open(file_name) as in_file:
        return json.load(in_file)

def updateMasterJSON(master_json, tokenNum, tokenData):
    pass
