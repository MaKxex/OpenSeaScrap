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
    """
        Получение твиттер, баланс дебанка, проверка его баланса владельца NFT
    """
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
        tmp = load_json("./sorted_data/" + filename)
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
        save_json("./sorted_data/" + filename,tmp)

