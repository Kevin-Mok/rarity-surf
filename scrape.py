from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from time import sleep

INITIAL_SLEEP = 7
TOKEN_ID_PREFIX = "The Sevens #"

def getRankBoxDiv(driver):
    flex_wrap_divs = driver.find_elements_by_class_name("flex-wrap")
    for flex_wrap_div in flex_wrap_divs:
        try:
            flex_wrap_div.find_element_by_class_name("font-extrabold")
            return flex_wrap_div
        except NoSuchElementException:
            print("No font-extrabold elem")

def getDriver(link, headless=False):
    options = Options()
    #  options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(link)
    return driver

def printSleep(seconds):
    print(f"Sleep: {seconds}s")
    for i in range(seconds):
        print(i)
        sleep(1)
    print("Done sleeping.")

def updateRankDict(rank_dict, rank_box_div):
    rank_boxes = rank_box_div.find_elements_by_class_name("bgCard")
    for rank_box in rank_boxes:
        #  rank = rank_box.find_element_by_class_name("font-extrabold").text
        token_id = rank_box.\
                find_element_by_partial_link_text("#").\
                text.removeprefix(TOKEN_ID_PREFIX)
        rank_dict[len(rank_dict) + 1] = token_id

if __name__ == "__main__":
    link = "https://rarity.tools/the-sevens-official"
    #  link = "file:///home/kevin/tmp/7s-rarity.tools.html"
    driver = getDriver(link)
    printSleep(INITIAL_SLEEP)

    rank_dict = {}
    updateRankDict(rank_dict, getRankBoxDiv(driver))
    pprint(rank_dict)
    driver.close()
