# ============================================================
# Level 2 - Task 2: Data Scraper
# Codveda Python Development Internship
#
# Scrapes the top stories from Hacker News (news.ycombinator.com)
# — a publicly scrapable site — and saves them to a CSV file.
#
# Install dependencies first:
#   pip install requests beautifulsoup4
# ============================================================

import csv
import sys
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit(
        "[Error] Missing dependencies.\n"
        "Run:  pip install requests beautifulsoup4"
    )

TARGET_URL = "https://news.ycombinator.com/"
OUTPUT_FILE = "scraped_headlines.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; CodvedaScraper/1.0)"
    )
}

def fetch_page(url):
    """Download a web page and return its text content."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()           # raises for 4xx / 5xx
        return response.text
    except requests.exceptions.ConnectionError:
        raise ConnectionError(f"Could not connect to {url}. Check your internet connection.")
    except requests.exceptions.Timeout:
        raise TimeoutError(f"Request to {url} timed out.")
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP error: {e}")

def parse_stories(html):
    """
    Parse Hacker News HTML and return a list of story dicts:
      rank, title, link, score, comments
    """
    soup = BeautifulSoup(html, "html.parser")
    stories = []

    title_rows  = soup.select("tr.athing")
    detail_rows = soup.select("tr.athing + tr")   # sibling rows with score/comment info

    for title_row, detail_row in zip(title_rows, detail_rows):
        rank_tag  = title_row.select_one("span.rank")
        link_tag  = title_row.select_one("span.titleline > a")
        score_tag = detail_row.select_one("span.score")
        comments_tag = detail_row.select("a")

        rank     = rank_tag.text.rstrip(".").strip() if rank_tag  else "?"
        title    = link_tag.text.strip()             if link_tag  else "N/A"
        link     = link_tag["href"]                  if link_tag  else "N/A"
        score    = score_tag.text.strip()            if score_tag else "0 points"

        # The last <a> in the detail row is normally the comments link
        comments = "0"
        if comments_tag:
            last_a = comments_tag[-1].text.strip()
            if "comment" in last_a:
                comments = last_a.split()[0]

        stories.append({
            "rank":     rank,
            "title":    title,
            "link":     link,
            "score":    score,
            "comments": comments,
        })

    return stories

def save_to_csv(stories, filepath):
    """Write a list of story dicts to a CSV file."""
    fieldnames = ["rank", "title", "link", "score", "comments"]
    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stories)

def main():
    print("=" * 55)
    print("   Hacker News Headline Scraper")
    print("=" * 55)
    print(f"  Source  : {TARGET_URL}")
    print(f"  Output  : {OUTPUT_FILE}")
    print(f"  Time    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)

    print("Fetching page …")
    try:
        html = fetch_page(TARGET_URL)
    except (ConnectionError, TimeoutError, RuntimeError) as e:
        print(f"[Error] {e}")
        return

    print("Parsing stories …")
    stories = parse_stories(html)

    if not stories:
        print("[Warning] No stories found. The site structure may have changed.")
        return

    save_to_csv(stories, OUTPUT_FILE)

    print(f"\nScraped {len(stories)} stories:\n")
    print(f"  {'#':<4}  {'Score':<14} {'Comments':<10} Title")
    print("-" * 55)
    for s in stories:
        title_short = s["title"][:45] + "…" if len(s["title"]) > 45 else s["title"]
        print(f"  {s['rank']:<4} {s['score']:<14} {s['comments']:<10} {title_short}")

    print(f"\n✅ Data saved to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
