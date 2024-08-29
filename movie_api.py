import pandas as pd
import re
import requests
import time
import random

file_path = r'C:\Users\JACK\Desktop\輔仁碩班\商業智慧\Move_2019_URL copy.csv'
df = pd.read_csv(file_path, encoding='utf-8-sig')

pattern = r"/movie/(\d+)"

urls = df['Href']

extracted_ids = [re.search(pattern, url).group(1) for url in urls if re.search(pattern, url)]


API_KEY = "50f3cd79ee65ff66e4cd0586a0d79efe"

def get_production_companies(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    attempts = 0
    while attempts < 5:  
        response = requests.get(url)
        if response.status_code == 200:
            movie_details = response.json()
            production_companies = movie_details.get('production_companies', [])
            company_names = [company.get('name') for company in production_companies]
            return company_names if company_names else None
        elif response.status_code == 429:  
            print("達到速率限制，等待一段時間...")
            time.sleep(30)  
        else:
            print(f"請求失敗，狀態碼: {response.status_code}")
            time.sleep(5)  
        attempts += 1
    return None  

companies = []
for movie_id in extracted_ids:
    company_names = get_production_companies(movie_id)
    if company_names:
        companies.append(", ".join(company_names)) 
    else:
        companies.append("NA") 
    random_sleep = random.uniform(1.5, 3.5)  
    time.sleep(random_sleep)

df['production_company'] = companies

df.to_csv(file_path, index=False, encoding='utf-8-sig')

print(f"結果已寫入 {file_path}")