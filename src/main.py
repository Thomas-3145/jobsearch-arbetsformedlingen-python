# main.py
# Hämtar jobb från arbetsförmedlingen och sparar till Excel


import os
import re
import yaml
import pandas as pd
from datetime import datetime
from api import fetch_jobs


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _whole_word_match(word, text):
    return bool(re.search(r'\b' + re.escape(word.lower()) + r'\b', text))


def check_if_relevant(title, company, include_words, exclude_words, required_words=None):
    text = f"{title} {company}".lower()
    if required_words and not any(_whole_word_match(w, text) for w in required_words):
        return False
    has_include = any(word.lower() in text for word in include_words)
    has_exclude = any(word.lower() in text for word in exclude_words)
    return has_include and not has_exclude


def get_jobs(keywords, locations, limit):
    all_jobs = []
    seen_urls = set()

    for keyword in keywords:
        for location in locations:
            print(f"Söker '{keyword}' i {location}...")

            jobs = fetch_jobs(keyword, location, limit)

            for job in jobs:
                url = job.get("webpage_url", "")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)

                workplace = job.get("workplace_address") or {}
                employer = job.get("employer") or {}
                clean_keyword = ' '.join(w for w in keyword.split() if not w.startswith('-'))

                all_jobs.append({
                    "keyword": clean_keyword,
                    "title": job.get("headline", ""),
                    "company": employer.get("name", ""),
                    "location": workplace.get("municipality", ""),
                    "url": url,
                    "published": job.get("publication_date", ""),
                })

    return all_jobs


def main():
    print("Startar...")

    config = load_config()
    keywords = config["keywords"]
    locations = config["locations"]
    limit = config.get("limit", 50)
    include_words = config.get("include_words", [])
    exclude_words = config.get("exclude_words", [])
    required_words = config.get("required_words", [])

    jobs = get_jobs(keywords, locations, limit)

    if not jobs:
        print("Hittade inga jobb")
        return

    print("Filtrerar...")
    filtered_jobs = [
        job for job in jobs
        if check_if_relevant(job["title"], job["company"], include_words, exclude_words, required_words)
    ]
    print(f"Hittade {len(filtered_jobs)} relevanta jobb")

    base = os.path.join(os.path.dirname(__file__), "..")
    csv_file = os.path.join(base, "jobs.csv")
    excel_file = os.path.join(base, "jobs.xlsx")

    # Läs gamla jobb
    old_urls = set()
    if os.path.exists(csv_file):
        try:
            old_data = pd.read_csv(csv_file, encoding="utf-8-sig")
            old_urls = set(old_data["url"].dropna().str.strip())
        except (FileNotFoundError, KeyError):
            pass

    new_jobs = [job for job in filtered_jobs if job["url"] not in old_urls]

    if not new_jobs:
        print("Inga nya jobb, filen ändras inte")
        return

    print(f"Hittade {len(new_jobs)} nya jobb att lägga till")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    for job in new_jobs:
        job["date_added"] = now

    # Bygg DataFrame: gamla + nya
    if os.path.exists(csv_file):
        old_df = pd.read_csv(csv_file, encoding="utf-8-sig")
        df = pd.concat([old_df, pd.DataFrame(new_jobs)], ignore_index=True)
    else:
        df = pd.DataFrame(new_jobs)

    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
    df.to_excel(excel_file, index=False, engine='openpyxl')

    print(f"Klart! Sparade {len(new_jobs)} nya jobb")


if __name__ == "__main__":
    main()
