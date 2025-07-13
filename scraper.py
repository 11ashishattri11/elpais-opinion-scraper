import os
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from collections import Counter
from urllib.parse import urljoin

BASE_URL = "https://elpais.com"
OPINION_SECTION = "/opinion/"
translator = Translator()
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_opinion_articles():
    res = requests.get(urljoin(BASE_URL, OPINION_SECTION), headers=HEADERS)
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = soup.select('article a[href*="/opinion/"]')[:5]
    article_data = []

    for a in articles:
        article_url = urljoin(BASE_URL, a['href'])
        article_res = requests.get(article_url, headers=HEADERS)
        article_soup = BeautifulSoup(article_res.text, 'html.parser')

        title_tag = article_soup.find("h1")
        paragraphs = article_soup.find_all("p")
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"
        content = "\n".join(p.get_text(strip=True) for p in paragraphs)

        image_tag = article_soup.find("img")
        image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else None

        if image_url:
            try:
                img_data = requests.get(image_url).content
                filename = title[:30].replace(" ", "_").replace("/", "_") + ".jpg"
                with open(filename, 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                print(f"Failed to download image: {e}")

        article_data.append({
            'title': title,
            'content': content,
            'image': image_url,
            'url': article_url
        })

    return article_data

def translate_titles(articles):
    for article in articles:
        translation = translator.translate(article['title'], src='es', dest='en')
        article['translated_title'] = translation.text
    return articles

def analyze_titles(articles):
    all_words = []
    for article in articles:
        words = article['translated_title'].lower().split()
        all_words.extend(words)

    counter = Counter(word for word in all_words if all_words.count(word) > 2)
    print("\nRepeated Words (More than twice):")
    for word, count in counter.items():
        print(f"{word}: {count}")

def print_articles(articles):
    for idx, article in enumerate(articles, 1):
        print(f"\n--- Article {idx} ---")
        print(f"Original Title: {article['title']}")
        print(f"Content (First 300 chars): {article['content'][:300]}...")
        print(f"Translated Title: {article['translated_title']}")
        print(f"Image saved: {'Yes' if article['image'] else 'No'}")

def main():
    print("Fetching articles from El País...")
    articles = get_opinion_articles()
    print("Translating article titles...")
    translated = translate_titles(articles)
    print_articles(translated)
    analyze_titles(translated)


if __name__ == "__main__":
    main()
