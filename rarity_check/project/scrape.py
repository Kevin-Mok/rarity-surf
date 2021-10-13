from project.cache import cache_json, read_json 
from project.constants import TOOLS_RANKS_FILE

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from sys import argv
from time import sleep

TOOLS_URL = "https://rarity.tools"
#  COLLECTION_NAME = "the-sevens-official"
#  COLLECTION_NAME = "mightybabydragons"
COLLECTION_NAME = "0n1-force"
COLLECTION_URL = f"{TOOLS_URL}/{COLLECTION_NAME}"

INITIAL_SLEEP = 10
SLEEP_BTWN_PAGES = 2
SLEEP_FOR_UPDATE = 5
TOKEN_ID_PREFIX = "The Sevens #"

def getRankBoxDiv(driver):
    flex_wrap_divs = driver.find_elements_by_class_name("flex-wrap")
    for flex_wrap_div in flex_wrap_divs:
        try:
            flex_wrap_div.find_element_by_class_name("font-extrabold")
            return flex_wrap_div
        except NoSuchElementException:
            pass

def getDriver(link, headless=False):
    options = Options()
    #  options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(link)
    pageSleep("intial", INITIAL_SLEEP)
    return driver

def pageSleep(page, seconds):
    print(f"Page {page} sleep: {seconds}s")
    for i in range(seconds):
        #  print(i)
        sleep(1)
    print("Done sleeping.")

def updateRankDict(rank_dict, rank_box_div):
    rank_boxes = rank_box_div.find_elements_by_class_name("bgCard")
    for rank_box in rank_boxes:
        rank = str(len(rank_dict) + 1)
        raw_token_id = rank_box.\
                find_element_by_partial_link_text("#").\
                text
        rank_dict[rank] = getTokenID(raw_token_id)

def nextPage(driver, page):
    page_div = driver.find_element_by_class_name("smallNoBtn")
    page_input = page_div.find_element_by_class_name("textInput")
    page_input.clear()
    page_input.send_keys(page)
    pageSleep(page, SLEEP_BTWN_PAGES)

def getToolsPageAtRank(rank):
    return f"{COLLECTION_URL}?filters=%24minRank%24{rank}%3Atrue"

def updateRankDictMult(driver, rank_dict, pages):
    for page in range(pages):
        updateRankDict(rank_dict, getRankBoxDiv(driver))
        print(f"Scraped {len(rank_dict)} ranks.")
        nextPage(driver, page + 2)
        #  pageSleep("update", SLEEP_FOR_UPDATE)
        cacheRankDict()
    driver.close()

def popRanks(start_rank, end_rank):
    for rank in range(start_rank, end_rank):
        rank_dict.pop(str(rank))

def loadRankDict():
    rank_dict = read_json(TOOLS_RANKS_FILE)
    print(f"Loaded {len(rank_dict)} ranks.")
    return rank_dict

def cacheRankDict():
    cache_json(rank_dict, TOOLS_RANKS_FILE)
    print(f"Cached {len(rank_dict)} ranks.")

def getTokenID(raw_token_id):
    return (raw_token_id[raw_token_id.rindex("#") + 1:] 
            if "#" in raw_token_id
            else raw_token_id)

def cleanTokenIDs():
    for rank, token_id in rank_dict.items():
        rank_dict[rank] = getTokenID(token_id)

if __name__ == "__main__":
    rank_dict = loadRankDict()
    driver = getDriver(getToolsPageAtRank(
        len(rank_dict) + 1))
    updateRankDictMult(driver, rank_dict, int(argv[1]))
