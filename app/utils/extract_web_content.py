import requests
from bs4 import BeautifulSoup
import time

def extract_web_content(url: list, delay=1):
    print(f"URL: {url}")
    time.sleep(delay)  # ここでリクエスト間の遅延を設定しています
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")

        # タグによって記事本文が異なる場合があるため、複数のタグを試してみてください
        article_tags = ["article", "main", "div"]

        for tag in article_tags:
            article = soup.find(tag)
            if article:
                return article.get_text(strip=True)
        
        # 本文が見つからなかった場合
        return "記事の本文が見つかりませんでした。"

    else:
        return f"Error {response.status_code}: Unable to fetch the webpage."
