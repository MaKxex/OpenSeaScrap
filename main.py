from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import undetected_chromedriver as uc
import time

from opensea import OpenseaAPI


# options = uc.ChromeOptions() 
# options.headless = False 
# driver = uc.Chrome(options=options) 


# driver.get(TWITTER_LOGIN_URL)
# time.sleep(5)


# driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input").send_keys(TWITTER_LOGIN)
# driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div").click()
# time.sleep(2)
# driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input").send_keys(TWIITER_NICKNAME)
# driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div").click()
# time.sleep(1)
# driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input").send_keys(TWITTER_PASSWORD)
# time.sleep(1)
# driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div").click()
# WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div/div/div/div/div/div/h2/span")))

# driver.get("https://opensea.io/rankings?sortBy=total_volume")


from opensea import OpenseaAPI

# create an object to interact with the Opensea API (need an api key)
api = OpenseaAPI(apikey=OPENSEA_API_KEY)
result = api.assets(owner="0xce90a7949bb78892f159f428d0dc23a8e3584d75",
                    limit=3)
print(result)


#--------------------------
# def scroll_to_end():
#     last_height = driver.execute_script("return document.body.scrollHeight")

#     while True:
#         yield
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         time.sleep(2)
#         new_height = driver.execute_script("return document.body.scrollHeight")
    

#         if new_height == last_height:
#             return False

#         last_height = new_height


# def scrap_Users_from_NFT(url_page):
#     tmp = {}
#     driver.get(url_page)
#     driver.find_element(By.XPATH, "//*[@id='main']/div/div/div/div[5]/div/div[5]/div/div/div/div[5]/div/div/button[1]").click()

#     scrolling = scroll_to_end()
#     flag = True
#     while flag:
#         list_of_image_record = WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role='table'] > div")))
#         print(len(list_of_image_record))
#         for image in list_of_image_record:
#             NFT_NAME = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a[data-testid='ItemCardFooter-name']"))).text
#             print(NFT_NAME)
#             tmp[NFT_NAME] = "a"
#             print(tmp)

#         next(scrolling)

# if __name__ == "__main__":
#     scrap_Users_from_NFT("https://opensea.io/collection/boringapesnft")



