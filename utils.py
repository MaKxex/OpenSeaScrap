import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re

def scroll_up(driver,repeats:int = 1):
    """
        Прокручивает страничку вверх
    """
    for _ in range(repeats):
        ActionChains(driver).send_keys(Keys.PAGE_UP).perform()


def scroll_down(driver,repeats:int = 1):
    """
        Прокручивает страничку вниз
    """
    for _ in range(repeats):
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()


def save_json(name,data):
    with open(f"{name}.json","w" ,encoding="utf8") as f:
        json.dump(data,f,indent=2)

def load_json(name):
    try:
        with open(f"{name}.json","r", encoding="utf8") as f:
            return json.load(f)
        
    except FileNotFoundError:
        print(name)
        with open(f"{name}.json", "w" ,encoding="utf8") as f:
            json.dump({},f)


def get_digits(string):
    return int("".join(re.findall(r"\d+",string.split("\n")[0])))

