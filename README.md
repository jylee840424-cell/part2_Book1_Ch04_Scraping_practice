# Books to Scrape 스크래핑 → LLM용 JSONL 생성

`https://books.toscrape.com/` 첫 페이지의 도서 정보를 수집하고,
일부 도서(기본 10권)의 상세페이지에서 카테고리/설명/UPC/리뷰 수를 추가로 수집한 뒤,
LLM 입력에 적합한 JSONL 파일(`books_scraping_llm.jsonl`)로 저장합니다.

---

## 기능 요약

- 첫 페이지 도서 카드(기본 20권) 수집
  - title, price, availability, rating, detail_url
- 상세페이지 수집(기본 앞 10권)
  - category, description, upc, num_reviews
- 결과를 LLM 친화 구조로 변환하여 JSONL로 저장

---

## 요구사항

- Python 3.9+ 권장
- 라이브러리 설치:

```bash
pip install requests beautifulsoup4 pandas

