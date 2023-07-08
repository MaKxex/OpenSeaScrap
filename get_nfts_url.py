from selenium.webdriver.support.ui import WebDriverWait
from config import OPENSEA_TOP_LIST_NFTS
from utils import scroll_down, save_json
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_all_nfts_url(driver):
    """
        Получение ссылок нфт из топ листа на главной страничке
    """
    tmp:set = set()
    driver.get(OPENSEA_TOP_LIST_NFTS)
    nextButton = True
    i = 1
    try:
        while nextButton:
            nfts_list = WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role='table'] > div")))
            for nft in nfts_list:
               tmp.add(nft.find_element(By.TAG_NAME, "a").get_attribute("href"))

            print(len(tmp))
            scroll_down()
            time.sleep(1)

            if len(driver.find_elements(By.XPATH, "//*[@id='main']/div/div[2]/button")) != 2:
                nextButton = False
            if (len(tmp) // (100 * i)) == 1:
                i +=1
                driver.find_elements(By.XPATH, "//*[@id='main']/div/div[2]/button")[1].click()
        
        save_json("nfts_list",list(tmp))

    except Exception as e:
        print(e)
        save_json("nfts_list",list(tmp))

        # last_height = new_height
        # if new_height == last_height: