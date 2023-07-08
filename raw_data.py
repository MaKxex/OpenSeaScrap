
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException, StaleElementReferenceException
import undetected_chromedriver as uc
import time
import re
from utils import load_json, save_json, get_digits,scroll_down, scroll_up

class OpenSea_accs:

    def __init__(self) -> None:
        options = uc.ChromeOptions() 
        options.headless = False
        self.driver = uc.Chrome(options=options) 

    def rollback(self):
        scroll_up(self.driver, 20)
        time.sleep(1)
        scroll_down(self.driver, 20)


    def parse_raw_opensea_accaunts(self,url_page):
        """
            Открывает конкретную нфт и получает ссылки на аккаунт владельца отдельной нфт
        """
        #TODO Сделать остановку этой адской машины
        self.driver.get(url_page)
        time.sleep(0.5)
        try:
            name = self.driver.find_element(By.CSS_SELECTOR, "div[class='media-greaterThanOrEqual-sm'] >h1").text
            self.driver.find_element(By.XPATH, "//*[@id='main']/div/div/div/div[5]/div/div[5]/div/div/div/div[5]/div/div/button[1]").click()
            new_name = re.sub('[^a-zA-Z0-9 \n\.]', '', name).replace(" ", "")
            flag = True
        except NoSuchElementException:
            return

        #last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.set_window_size(1920/2,1080/2)
        stale_num = 1
        while flag:
            try:
                print(stale_num)

                if stale_num % 10 == 0:
                    self.rollback()
                    scroll_down(self.driver, 2)

                if stale_num % 20 == 0:
                    scroll_down(self.driver, 10)
                    self.rollback()

                if stale_num == 100:
                    break
                
                tmp = load_json("./raw_nft_accs/" + new_name)
                list_of_image_record = WebDriverWait(self.driver,20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[role='table'] > div")))
                for image in list_of_image_record:
                    NFT_id = image.find_element(By.CSS_SELECTOR, "a[data-testid='ItemCardFooter-name']").get_attribute("href").split("/")[-1]
                    tmp[NFT_id] = image.find_element(By.CSS_SELECTOR, "a[class*='AccountLink--ellipsis-overflow']").get_attribute("href")


                
                scroll_down(self.driver,2)
                #new_height = self.driver.execute_script("return document.body.scrollHeight")

                save_json("./raw_nft_accs/" + new_name,tmp)

                # if new_height == last_height:
                #     break

                # last_height = new_height

                stale_num = 1


            except StaleElementReferenceException:
                stale_num += 1

            except NoSuchElementException:
                stale_num += 1

            except NoSuchWindowException:
                break

            except Exception as e:
                print(e)
            
    def run(self,url):
        self.parse_raw_opensea_accaunts(url)