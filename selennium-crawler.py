from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import pandas as pd

#參數
keyword="外套"
page="0"
user="0975873880"
password="zscfbhjm12"

#建立Driver 物件實體，用程式操作瀏覽器運作
driver = webdriver.Chrome()

#連線網址
driver.get("https://shopee.tw/search?keyword=" + keyword + "&page=" + page)

#等待10秒，到找到元素
driver.implicitly_wait(30)

#登入
driver.find_element(By.CSS_SELECTOR, 'input[name="loginKey"]').send_keys(user)
driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
time.sleep(3)

login=driver.find_elements(By.CSS_SELECTOR, 'button')[2].click()

time.sleep(10)


#搜尋物品

items = driver.find_elements(By.CLASS_NAME, 'Cve6sh')
for item in items:



# parent_element = driver.find_elements(By.CLASS_NAME, 'row shopee-search-item-result__items')
# titletags=driver.find_elements(By.CLASS_NAME, 'Cve6sh')[0].text


# driver.close()


