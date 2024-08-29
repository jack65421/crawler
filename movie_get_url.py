from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys

#參數
start_year="2018/01/01"
end_year="2018/12/31"


# 建立Driver 物件實體，用程式操作瀏覽器運作
driver = webdriver.Chrome()

# 連線網址
driver.get("https://www.themoviedb.org/movie?language=zh-TW")


#滾動
def scroll_to_bottom(driver, scroll_increment=200, scroll_delay=0.5, additional_check_time=10):
    """
    逐步滾動至網頁底部，確保動態內容充分加載，並增加重複檢查機制來確認是否真的到達底部。

    Args:
    driver (webdriver): Selenium webdriver 實例。
    scroll_increment (int): 每次滾動的像素高度。
    scroll_delay (float): 每次滾動後的等待時間，以秒計。
    additional_check_time (float): 在初次到達底部時再等待一段時間，以確認是否真的到達底部。
    """
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 逐步向下滾動
        for i in range(0, last_height, scroll_increment):
            driver.execute_script(f"window.scrollTo(0, {i});")
            time.sleep(scroll_delay)

        # 暫停時間，讓頁面加載
        time.sleep(scroll_delay)

        # 檢查是否到達底部
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # 如果高度沒有變化，等待額外的時間再檢查一次
            time.sleep(additional_check_time)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # 如果再次檢查後高度仍沒有變化，則認為已到達底部
        last_height = new_height
      
# 選擇排序條件
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".filter_panel.card.closed"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".k-dropdown-wrap.k-state-default"))).click()

# 選擇發行日期降序
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".k-list-container .k-item[data-offset-index='0']"))).click()

#關閉彈跳視窗
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon"))).click()

#篩選條件
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "all_releases"))).click()
time.sleep(1)
checkbox_labels=driver.find_elements(By.CLASS_NAME,"k-checkbox-label")
for label in checkbox_labels:    
    if label.is_displayed() and label.text.strip() != '搜索所有发行渠道？'and label.text.strip() != '首映' and label.text.strip() != '电影院上映':  # 確保元素是可見的與想要篩選的條件，才進行點擊操作
            label.click()

 # 定位到時間輸入框
driver.find_element(By.ID, "release_date_gte").send_keys(start_year)
# 清空輸入框
date_input=driver.find_element(By.ID, "release_date_lte")
date_input.clear()

# 輸入新的時間區間值
date_input.send_keys(end_year)
#移動焦點到下一個點
date_input.send_keys(Keys.TAB)

#搜尋位置
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.no_click.load_more")))

time.sleep(1)

# 使用 JavaScript 執行點擊
select_more = driver.find_element(By.CSS_SELECTOR, "a.no_click.load_more")
driver.execute_script("arguments[0].click();", select_more)

#滾動
scroll_to_bottom(driver)

#點擊載入更多
load_more_elements=driver.find_elements(By.CSS_SELECTOR, "a.no_click.load_more")

for load_more_element in load_more_elements:
    if load_more_element.text == "载入更多":
        load_more_element.click()

#滾動
scroll_to_bottom(driver)

time.sleep(2)

df = pd.DataFrame(columns = ["Title", "Href", "Type"])
data_list=[]

#get url
try:
    # 等待页面加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".media_items.results"))
    )

    # 獲取所有頁面
    pages = driver.find_elements(By.CSS_SELECTOR, ".page_wrapper")
    for page in pages:
        movie_cards = page.find_elements(By.CSS_SELECTOR, ".card.style_1")
        for card in movie_cards:
            # 確保每個卡片中都有'h2 a'選擇器可以選擇到
            links = card.find_elements(By.CSS_SELECTOR, "h2 a")
            if not links:
                continue  
            href = links[0].get_attribute("href")
            title = links[0].text
            # data_percent = card.find_elements(By.CSS_SELECTOR, ".user_score_chart")[0].get_attribute("data-percent")
            # date_texts = card.find_elements(By.CSS_SELECTOR, ".content p")
            # date_time = date_texts[0].text if date_texts else "No date provided" 
            data_list.append({
                "Title": title,
                "Href": href,
                "Type": "Pending"
            })


except Exception as e:
    print(f"An error occurred: {e}")

df = pd.DataFrame(data_list)

df.to_csv('Move_2018_URL.csv', index=False, encoding='utf-8-sig')


