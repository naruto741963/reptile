import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, timedelta
import re

toDay = str(date.today())[5:].replace("-", "/")
endDay = str(date.today() - timedelta(days=8))[5:].replace("-", "/")

toDayFlag = False
session = requests.Session()
# my_cookie = {}
data = {"from": "/bbs/Gossiping/index.html",
        "yes": "yes"}
my_header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
url = "https://www.ptt.cc/ask/over18"
session.post(url, headers=my_header, data=data)

url2 = "https://www.ptt.cc/bbs/Gossiping/index.html"

while True:
    r = session.get(url2)
    if r.status_code == 200:
        r2 = r.text.split("r-list-sep")[0]
        soup = BeautifulSoup(r2, "html.parser")
        titles = soup.select("div.title a")
        dates = soup.select("div.date")

        newUrl = "https://www.ptt.cc" + soup.select("div.btn-group.btn-group-paging a")[1].get("href")
        user_ids = []
        contents = []
        times = []

        for title, date in zip(titles, dates):
            if date.text.strip() not in toDay:
                toDayFlag = True
                continue

            inUrl = "https://www.ptt.cc" + title.get("href")
            r3 = session.get(inUrl)
            soup3 = BeautifulSoup(r3.text, "html.parser")
            span = soup3.select("span.article-meta-value")
            text = soup3.select_one("div#main-content").text.split("※ 發信站: 批踢踢實業坊(ptt.cc)")[0].split(span[3].text)[1]
            message = soup3.select("div.push")
            for msg in message:
                user_id = msg.find("span", class_="f3 hl push-userid").text.strip()
                content = msg.find("span", class_="f3 push-content").text.strip(": ").strip()
                time = msg.find("span", class_="push-ipdatetime").text.strip()
                user_ids.append(user_id)
                contents.append(content)
                times.append(time)
            data = {"作者": [span[0].text], "標題": [span[2].text], "發文時間": [span[3].text], "內文": [text],
                 "類別": [span[1].text], "留言作者": user_ids, "留言內文": contents, "留言時間": times}
            df = pd.DataFrame.from_dict(data, orient='index').T
            df = df.applymap(lambda x: str(x) if not isinstance(x, str) else x)
            df = df.applymap(lambda x: x.encode('big5', 'replace').decode('big5'))
            filename = re.sub(r'[<>:"/\\|?*]', '_', span[2].text) + ".csv"
            df.to_csv(f"{filename}.csv", encoding="big5")
        if toDayFlag == True:
            break
        url2 = newUrl