import requests
import time
import random
import os

COMMON_SUBJECTS = [
    "computer_science",
    "history",
    "science_fiction",
    "children",
    "romance",
    "psychology",
    "mathematics",
    "art",
    "biography",
    "business"
]

EXTRA_SUBJECTS = [
    "technology", "medicine", "sports", "education", "philosophy",
    "travel", "music", "nature", "self_help", "politics"
]

def fetch_isbn_from_subject(subject, count=10):
    isbns = set()
    
    url = f"https://openlibrary.org/subjects/{subject}.json?limit={count},published_in=2015-2025"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"❌ 主題 {subject} 擷取失敗: {e}")
        return []

    works = data.get("works", [])

    for work in works:
        time.sleep(0.3)
        editions_url = f"https://openlibrary.org{work['key']}/editions.json?limit=10"
        try:
            res = requests.get(editions_url)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f"  ⚠️ 無法讀取 work {work['key']} editions: {e}")
            continue

        url = f"https://openlibrary.org/books/{work['cover_edition_key']}.json"
        res = requests.get(url)
        cover_edition = res.json()

        if "isbn_13" in cover_edition:
            isbns.update(cover_edition["isbn_13"])
        elif "isbn_10" in cover_edition:
            isbns.update(cover_edition["isbn_10"])

    print(f"✅ 從科目 {subject} 獲取 {len(isbns)} 本書")
    return list(isbns)[:count]


def fetch_multiple_subjects(subjects, per_subject_count=10, save_path=os.path.join("app", "data", "isbn_list.txt")):
    all_isbns = set()

    for subject in subjects:
        subject_isbns = fetch_isbn_from_subject(subject, per_subject_count)
        all_isbns.update(subject_isbns)

    while len(all_isbns) < len(subjects) * per_subject_count:
        extra_subject = random.choice(EXTRA_SUBJECTS)
        print(f"🌀 額外補足主題：{extra_subject}")
        subject_isbns = fetch_isbn_from_subject(extra_subject, per_subject_count)
        all_isbns.update(subject_isbns)

    with open(save_path, "w", encoding="utf-8") as f:
        for isbn in all_isbns:
            f.write(isbn + "\n")
    print(f"\n📁 所有 isbn 已儲存到 {save_path}（總共 {len(all_isbns)} 本）")


if __name__ == "__main__":
    fetch_multiple_subjects(COMMON_SUBJECTS, per_subject_count=10)



'''
import requests
import json

subject = "science_fiction"
url = f"https://openlibrary.org/subjects/{subject}.json?limit=10"
res = requests.get(url)
data = res.json()

work = data.get("works", [])[2]
#print(json.dumps(work, indent=2, ensure_ascii=False))

url = f"https://openlibrary.org/books/{work['cover_edition_key']}.json"
res = requests.get(url)
data = res.json()


url = f"https://openlibrary.org/isbn/{data['isbn_13']}.json"
res = requests.get(url)
data = res.json()

print(json.dumps(data, indent=2, ensure_ascii=False))
'''

'''
#url = f"https://openlibrary.org/works/{work['cover_edition_key']}/editions.json"
url = f"https://openlibrary.org{work['key']}/editions.json?limit=2"
res = requests.get(url)
data = res.json()

edition = data.get("entries", [])[1]


url = f"https://openlibrary.org/isbn/{edition['isbn_13']}.json"
res = requests.get(url)
data = res.json()

print(json.dumps(data, indent=2, ensure_ascii=False))
'''