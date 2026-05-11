import requests
import time
import xml.etree.ElementTree as ET
from datetime import date
from groq import Groq

import os
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

TOPICS = [
    "large language models financial markets",
    "machine learning asset pricing",
    "AI algorithmic trading",
]

def fetch_papers(topic, max_results=3):
    url = "https://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{topic}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    response = requests.get(url, params=params, timeout=30)
    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        abstract = entry.find("atom:summary", ns).text.strip()[:500]
        link = entry.find("atom:id", ns).text.strip()
        papers.append({"title": title, "abstract": abstract, "url": link})
    return papers

def summarise_paper(title, abstract):
    client = Groq(api_key=GROQ_API_KEY)
    prompt = f"Summarise this paper in 2-3 sentences for a finance professional:\n\nTitle: {title}\n\nAbstract: {abstract}"
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    return response.choices[0].message.content

def main():
    print(f"\n=== ArXiv Digest — {date.today()} ===\n")
    for topic in TOPICS:
        papers = fetch_papers(topic)
        for paper in papers:
            print(f"📄 {paper['title']}")
            summary = summarise_paper(paper['title'], paper['abstract'])
            print(f"   {summary}")
            print(f"   {paper['url']}\n")
        time.sleep(5)

if __name__ == "__main__":
    main()
