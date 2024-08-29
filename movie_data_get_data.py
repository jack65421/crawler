import re
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# 初始化資料框架的標題
columns = ["Title", "Certification", "ReleaseDate", "Genres", "Runtime", "Budget", "BoxOffice", "Rate"]
data_list = []
url_list = []

# CSV 文件名
csv_file = 'Move_2020_URL.csv'


# 從 CSV 文件中讀取 URL
with open(csv_file, 'r', newline='', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    next(reader)  # 跳過標題行
    for row in reader:
        url_list.append(row[1])  



# 初始化 WebDriver
driver = webdriver.Chrome()

def process_movie_page(url):
    driver.get(url)
    try:
        # 關閉彈跳視窗
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".onetrust-close-btn-handler.onetrust-close-btn-ui.banner-close-button.ot-close-icon"))
            ).click()
        except (NoSuchElementException, TimeoutException):
            pass

        # 片名
        try:
            title_element = driver.find_element(By.CSS_SELECTOR, "h2 a")
            Title = title_element.text
        except NoSuchElementException:
            Title = "未提供"

        # 分級
        try:
            certification_element = driver.find_element(By.CSS_SELECTOR, ".facts .certification")
            Certification = certification_element.text
        except NoSuchElementException:
            Certification = "未提供"

        # 上映日期
        try:
            release_date_element = driver.find_element(By.CSS_SELECTOR, ".facts .release")
            ReleaseDate = release_date_element.text
        except NoSuchElementException:
            ReleaseDate = "未提供"

        # 分類
        try:
            genres_element = driver.find_element(By.CSS_SELECTOR, ".facts .genres")
            Genres = genres_element.text
        except NoSuchElementException:
            Genres = "未提供"

        # 時長
        try:
            runtime_element = driver.find_element(By.CSS_SELECTOR, ".facts .runtime")
            Runtime = runtime_element.text
        except NoSuchElementException:
            Runtime = "未提供"

        # 預算
        try:
            budget_elements = driver.find_elements(By.CSS_SELECTOR, ".facts.left_column p")
            budget_text = budget_elements[-2].text
            budget_match = re.search(r"([\d,\.]+)", budget_text.replace(",", ""))
            if budget_match:
                Budget = budget_match.group(1)
            else:
                Budget = "未提供"
        except NoSuchElementException:
            Budget = "未提供"

        # 票房
        try:
            box_office_elements = driver.find_elements(By.CSS_SELECTOR, ".facts.left_column p")
            box_office_text = box_office_elements[-1].text
            box_office_match = re.search(r"([\d,\.]+)", box_office_text.replace(",", ""))
            if box_office_match:
                BoxOffice = box_office_match.group(1)
            else:
                BoxOffice = "未提供"
        except NoSuchElementException:
            BoxOffice = "未提供"

        # 評分
        try:
            data_percent = driver.find_elements(By.CSS_SELECTOR, ".user_score_chart")[0].get_attribute("data-percent")
        except NoSuchElementException:
            data_percent = "未提供"

        time.sleep(1)

        return Title, Certification, ReleaseDate, Genres, Runtime, Budget, BoxOffice, data_percent
    
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

# 逐一處理 URL 列表中的每個網頁
for url in url_list:
    result = process_movie_page(url)
    if result:
        data_list.append(result)
    else:
        print(f"Skipped {url} due to an error.")

# 將資料列表轉換為 DataFrame 並保存為 CSV 文件
df = pd.DataFrame(data_list, columns=columns)
df.to_csv('Move_2020_data.csv', index=False, encoding='utf-8-sig')

# 關閉 WebDriver
driver.quit()
