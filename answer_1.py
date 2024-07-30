import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

session = requests.Session()
my_cookie = {}
my_header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
url = "https://www.ptt.cc/bbs/index.html"
r = session.get(url, headers=my_header, cookies=my_cookie)

boradName = []
urls = []

if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    div_tags = soup.find_all("div",class_="board-name")
    for div in div_tags:
        boradName.append(div.text)
    a_tags = soup.find_all("a",class_="board")
    for a in a_tags:
        url = "https://www.ptt.cc/" + a.get("href")
        urls.append(url)
print(boradName)
print("-------------------------------------")
print(urls)
df = pd.DataFrame({"列表名稱": boradName, "連結": urls})
try:
    df.to_csv("PTTborad.csv", encoding="big5")
except Exception as e:
    print(f"Error saving CSV: {e}")
