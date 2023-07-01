from config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions
import undetected_chromedriver as uc
import time
import re
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains

import json

options = uc.ChromeOptions() 
options.headless = False
driver = uc.Chrome(options=options) 


#TODO
# Распараллелить парс на несколько процессов, тем самым увеличив скорость обработки
# Переделать под обьктную базу
# Логгирование



def SignInTwitter():
    try:
        driver.get(TWITTER_LOGIN_URL)
    
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")))
        driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input").send_keys(TWITTER_LOGIN)
        driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div").click()
        
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")))
        driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input").send_keys(TWIITER_NICKNAME)
        driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div").click()

        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")))
        driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input").send_keys(TWITTER_PASSWORD)
        
        
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div")))
        driver.find_element(By.XPATH, "//*[@id='layers']/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div").click()
        WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[1]/div/div/div/div/div/div/h2/span")))

        driver.get("https://opensea.io/rankings?sortBy=total_volume")
        return True
    except Exception as e:
        print(e)
        return False

def scroll_to_end():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        yield
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
    

        if new_height == last_height:
            return False

        last_height = new_height

def save_json(name,data):
    with open(f"{name}.json","w" ,encoding="utf8") as f:
        json.dump(data,f,indent=2)

def load_json(name):
    try:
        with open(f"{name}.json","r", encoding="utf8") as f:
            return json.load(f)
        
    except FileNotFoundError:
        with open(f"{name}.json", "w" ,encoding="utf8") as f:
            json.dump({},f)


def get_digits(string):
    return int("".join(re.findall(r"\d+",string.split("\n")[0])))

def scrap_accUrl_from_nft_page(url_page):
    #TODO Сделать остановку этой адской машины
    #TODO Пофиксить ошибки, которые просто проглатываются
    #TODO Увеличить скороть парса
    driver.get(url_page)
    name = driver.find_element(By.CSS_SELECTOR, "div[class='media-greaterThanOrEqual-sm'] >h1").text
    driver.find_element(By.XPATH, "//*[@id='main']/div/div/div/div[5]/div/div[5]/div/div/div/div[5]/div/div/button[1]").click()
    flag = True
    while flag:
        try:
            tmp = load_json(name)
            time.sleep(10)
            list_of_image_record = WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role='table'] > div")))
            for image in list_of_image_record:
                NFT = image.find_element(By.CSS_SELECTOR, "a[data-testid='ItemCardFooter-name']")
                tmp[str(get_digits(NFT))] = image.find_element(By.CSS_SELECTOR, "a[class*='AccountLink--ellipsis-overflow']").get_attribute("href")
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            save_json(name,tmp)
        except Exception as e:
            print(e)


def get_user_twitter():
    try:
        href = driver.find_elements(By.CSS_SELECTOR, "div[class='media-greaterThanOrEqual-md'] > div > div > a")[-1].get_attribute("href")
        if href.startswith("https://twitter.com"):
            return href
        return None
    except selenium.common.exceptions.NoSuchElementException:
        return None
    except IndexError:
        return None
    
def get_user_wallet():
    pyperclip.copy('')
    try:
        wallet = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class*='cEtajt bphgzn']")))
        action_chains = ActionChains(driver)
        action_chains.move_to_element(wallet).perform()
        wallet.click()
        return pyperclip.paste()
    except selenium.common.exceptions.TimeoutException:
        try:
            WebDriverWait(driver,7).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "i[value='expand_more']"))).click()
            WebDriverWait(driver,7).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[class='tippy-content'] > div > ul > :nth-child(2)"))).click()
            return pyperclip.paste()
        except Exception as e:
            print(e)
            return None


def check_twitter_dm():
    try:
        WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='sendDMFromProfile']")))
        return True
    except selenium.common.exceptions.TimeoutException:
        return False




def get_debank_deposit():
    try:
        WebDriverWait(driver,15).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class*='AssetsOnChain_totalChain']")))
        return get_digits(WebDriverWait(driver,1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[class*='HeaderInfo_totalAssetInner']"))).text)
        #return get_digits(driver.find_element(By.CSS_SELECTOR, "div[class*='HeaderInfo_totalAssetInner']").text)
    except selenium.common.exceptions.NoSuchElementException:
        return None
    except selenium.common.exceptions.TimeoutException:
        return None


def check_debank_deposit():
    debank_deposit = get_debank_deposit()
    if not debank_deposit:
        return None
    if debank_deposit >= DEBANK_LOW_EDGE_DEPOSIT:
        return debank_deposit
    
    return False



class DeBank:
    pass


class OpenSea:
    pass


class Twitter:
    pass


class Scrapper:
    pass


def remove_proccesed_data(nft_json_name):
    data = load_json(nft_json_name)
    unprocessed_data = set(load_json(nft_json_name).keys())
    unprocessed_data_values = set(load_json(nft_json_name).values())
    processed_data =  load_json(nft_json_name+ "_sorted")

    for processed in processed_data.values():
        processed_opensea_url = processed.get("opensea_url")
        indexs_to_remove = []
        for index, val in enumerate(unprocessed_data_values):
            if val == processed_opensea_url:
                indexs_to_remove.append(index)

        for index in indexs_to_remove:
            del data[list(unprocessed_data)[index]]

    return unprocessed_data



def processing_data_from_nft_json(nft_json_name,offset=0):
    filename = nft_json_name + "_sorted"
    driver.set_window_size(1000,900)
    if not SignInTwitter():
        quit()

    tmp = {}

    data = load_json(nft_json_name)
    amount = len(list(set(data.values()))[offset:])
    #driver.options.add_argument("--headless")
    for index, url in enumerate(list(set(data.values()))[offset:]):
        print(f"processing {index + offset}/{amount}")
        tmp = load_json(filename)
        driver.get(url)
        twitter_url = get_user_twitter()
        if not twitter_url:
            continue

        wallet = get_user_wallet()

        if not wallet:
            continue

        driver.get(twitter_url)
        if not check_twitter_dm():
            continue
        
        driver.get(DEBANK_PROFILE + wallet)
        time.sleep(5)
        debank_deposit = check_debank_deposit()
        if not debank_deposit:
            continue
        
        tmp[twitter_url] = {
            "debank_deposit": debank_deposit,
            "opensea_url": url,
            "debank_url": DEBANK_PROFILE + wallet
        }
        save_json(filename,tmp)


if __name__ == "__main__":    
    processing_data_from_nft_json("Cool Cats NFT", 2000)
    #print(len(set(load_json("Cool Cats NFT"))))
    #print(len(remove_proccesed_data("Cool Cats NFT")))
        
    #scrap_accUrl_from_nft_page("https://opensea.io/collection/cool-cats-nft")



