from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

if __name__ == "__main__":
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    #  driver.get("https://rarity.tools/the-sevens-official")
    driver.get("file:///home/kevin/tmp/7s-rarity.tools.html")
    assert "rarity.tools" in driver.title
    #  rank_box_elems = driver.find_elements_by_class_name("bgCard")
    rank_box_elem = driver.find_element_by_xpath(
            "/html/body/")
    #  print(rank_box_elems)
    #  for rank_box_elem in rank_box_elems:
        #  try:
            #  rank_num_elem = rank_box_elem.find_element_by_class_name("font-extrabold")
        #  except NoSuchElementException:
            #  print("No font-extrabold elem")
    #  print(rank_num_elem.getText())
    driver.close()
