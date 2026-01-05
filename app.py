import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import json

url = "https://books.toscrape.com/"
response = requests.get(url, timeout=20)
response.raise_for_status()

html = response.text

soup = BeautifulSoup(html, "html.parser")

items = soup.select("article.product_pod")
print(len(items))  # 결과: 20

rows = []
BASE_URL = url
for item in items :
    a_tag = item.select_one("h3 a")
    title = a_tag["title"]
    
    relative_url = a_tag["href"]
    detail_url = BASE_URL + relative_url
    print(detail_url)
    
    price = item.select_one("p.price_color").get_text(strip=True)
    availability = item.select_one("p.instock.availability").get_text(" ", strip=True)

    rating_tag = item.select_one("p.star-rating")
    rating = rating_tag["class"][1]  # One, Two, Three, Four, Five

    rows.append({
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "detail_url": detail_url
    })


def parse_detail(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    s = BeautifulSoup(r.text, "html.parser")

    # 카테고리
    breadcrumb = s.select("ul.breadcrumb li a")
    category = breadcrumb[-1].get_text(strip=True)

    # 설명
    description = ""
    desc_header = s.select_one("#product_description")
    if desc_header:
        p = desc_header.find_next_sibling("p")
        if p:
            description = p.get_text(" ", strip=True)

    # 상품 정보 테이블
    info = {}
    for row in s.select("table.table.table-striped tr"):
        key = row.select_one("th").get_text(strip=True)
        value = row.select_one("td").get_text(strip=True)
        info[key] = value

    return {
        "category": category,
        "description": description,
        "upc": info.get("UPC"),
        "num_reviews": info.get("Number of reviews")
    }


for i, row in enumerate(rows[:10]):
    detail = parse_detail(row["detail_url"])
    row.update(detail)
    time.sleep(1)


df = pd.DataFrame(rows)

df["num_reviews"] = pd.to_numeric(df["num_reviews"], errors="coerce")
df["description"] = df["description"].fillna("")

def to_llm_record(row):
    return {
        "source": "books.toscrape.com",
        "title": row["title"],
        "category": row["category"],
        "price": row["price"],
        "rating": row["rating"],
        "availability": row["availability"],
        "num_reviews": row["num_reviews"],
        "description": row["description"]
    }


with open("books_scraping_llm.jsonl", "w", encoding="utf-8") as f:
    for _, row in df.iterrows():
        f.write(json.dumps(to_llm_record(row), ensure_ascii=False) + "\n")