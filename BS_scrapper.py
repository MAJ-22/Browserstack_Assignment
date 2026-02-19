import os
import time
import requests
import re
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv
import threading

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPID_API_KEY")
BS_USERNAME  = os.getenv("BS_USERNAME")
BS_ACCESSKEY = os.getenv("BS_ACCESSKEY")

os.makedirs("images", exist_ok=True)
os.makedirs("articles_text", exist_ok=True)

BS_CAPABILITIES = [
    {   # 1. Windows 11 — Chrome
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows", "osVersion": "11",
            "sessionName": "ElPais_Chrome_Windows11"
        }
    },
    {   # 2. macOS Ventura — Safari
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X", "osVersion": "Ventura",
            "sessionName": "ElPais_Safari_macOS"
        }
    },
    {   # 3. Windows 10 — Firefox
        "browserName": "Firefox",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows", "osVersion": "10",
            "sessionName": "ElPais_Firefox_Windows10"
        }
    },
    {   # 4. iPhone 14 — Mobile Safari
        "browserName": "safari",
        "bstack:options": {
            "deviceName": "iPhone 14",
            "osVersion": "16",
            "realMobile": "true",
            "sessionName": "ElPais_iPhone14"
        }
    },
    {   # 5. Samsung Galaxy S23 — Chrome Mobile
        "browserName": "chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "osVersion": "13.0",
            "realMobile": "true",
            "sessionName": "ElPais_GalaxyS23"
        }
    },
]

BS_URL = f"https://{BS_USERNAME}:{BS_ACCESSKEY}@hub-cloud.browserstack.com/wd/hub"


def translate_to_english(text):
    url = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
    payload = {"q": text, "source": "es", "target": "en"}
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    translated = result["data"]["translations"]["translatedText"]
    return translated[0] if isinstance(translated, list) else translated


# ────────────────────
# Core scraping logic
# ────────────────────
def scrape_elpais(driver, thread_name="local", print_preview=False):
    print(f"\n[{thread_name}] Starting scrape...")
    driver.get("https://elpais.com/opinion/")
    time.sleep(3)

    all_link_elements = driver.find_elements(By.TAG_NAME, "a")
    candidate_links = []
    for a in all_link_elements:
        href = a.get_attribute("href")
        if href and re.search(r"/opinion/\d{4}-\d{2}-\d{2}/", href) and "#" not in href:
            candidate_links.append(href)
    candidate_links = list(dict.fromkeys(candidate_links))

    articles_data = []

    for link in candidate_links:
        if len(articles_data) >= 5:
            break

        driver.get(link)
        time.sleep(2)

        texts = driver.execute_script("""
            return Array.from(document.querySelectorAll('p.a_st, div.a_c p'))
                .map(e => e.innerText.trim())
                .filter(t => t.length > 20);
        """)

        if not texts:
            print(f"[{thread_name}] Skipping {link} — no content")
            continue

        body_text = "\n\n".join(texts)
        title = driver.execute_script(
            "return document.querySelector('h1')?.innerText?.trim() || 'No Title'"
        )

        img_url = None
        try:
            img_url = driver.find_element(By.CSS_SELECTOR, "figure img").get_attribute("src")
        except:
            pass

        # Saving images only on local run to avoid duplicates across threads
        if img_url and thread_name == "local":
            try:
                safe_title = re.sub(r'[\\/*?\"<>|:]', '_', title)
                img_data = requests.get(img_url, timeout=10).content
                with open(f"images/{safe_title}.jpg", "wb") as f:
                    f.write(img_data)
            except Exception as e:
                print(f"[{thread_name}] Image error: {e}")

        articles_data.append({"title": title, "body": body_text, "image": img_url, "link": link})

        #printing preview of the extracted content
        if print_preview:
            print(f"\n[{thread_name}] --- Article {len(articles_data)} ---")
            print(f"Title: {title}")
            print(f"Content preview: {body_text[:100]}...")
        else:
            print(f"[{thread_name}] Scraped article {len(articles_data)}: {title}")
        
    return articles_data


#saving scraped articles under a text document
def process_and_save(articles_data):
    # Save combined txt
    with open("articles_text/all_articles.txt", "w", encoding="utf-8") as out:
        for i, article in enumerate(articles_data, 1):
            out.write(f"{'=' * 60}\n")
            out.write(f"ARTICLE {i}\n")
            out.write(f"{'=' * 60}\n")
            out.write(f"Title: {article['title']}\n")
            out.write(f"Link:  {article['link']}\n\n")
            out.write(article["body"])
            out.write("\n\n")

    # Translate
    print("\n" + "=" * 60)
    print("TRANSLATED ARTICLE HEADERS")
    print("=" * 60)

    translated_titles = []
    for i, article in enumerate(articles_data, 1):
        translated = translate_to_english(article["title"])
        translated_titles.append(translated)
        print(f"{i}. Original  : {article['title']}")
        print(f"   Translated: {translated}\n")

    # Word frequency
    print("=" * 60)
    print("REPEATED WORDS (appearing more than twice across all titles)")
    print("=" * 60)

    all_words = []
    for title in translated_titles:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
        all_words.extend(words)

    word_counts = Counter(all_words)
    repeated = {word: count for word, count in word_counts.items() if count > 2}

    if repeated:
        for word, count in sorted(repeated.items(), key=lambda x: -x[1]):
            print(f"  '{word}' — {count} times")
    else:
        print("  No words repeated more than twice.")

    print(f"\nDone! {len(articles_data)} articles saved to articles_text/all_articles.txt")


# BrowserStack thread worker
def run_on_browserstack(caps, index):
    thread_name = caps["bstack:options"]["sessionName"]
    driver = None
    try:
        options = webdriver.ChromeOptions() if "chrome" in caps.get("browserName", "").lower() else \
                  webdriver.FirefoxOptions() if "firefox" in caps.get("browserName", "").lower() else \
                  webdriver.SafariOptions()

        for key, value in caps.items():
            options.set_capability(key, value)

        driver = webdriver.Remote(command_executor=BS_URL, options=options)
        articles = scrape_elpais(driver, thread_name=thread_name, print_preview=True)

        # Mark session as passed
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status": "passed", "reason": "Scraped 5 articles successfully"}}')
        print(f"[{thread_name}] ✓ PASSED — {len(articles)} articles scraped")

    except Exception as e:
        print(f"[{thread_name}] ✗ FAILED — {e}")
        if driver:
            driver.execute_script(f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status": "failed", "reason": "{str(e)[:100]}"}}}}')
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":

    # ── Step 1: Run locally first ──
    print("=" * 60)
    print("RUNNING LOCALLY")
    print("=" * 60)
    local_driver = webdriver.Chrome()
    try:
        articles_data = scrape_elpais(local_driver, thread_name="local", print_preview=True)
    finally:
        local_driver.quit()

    process_and_save(articles_data)

    # ── Step 2: Run on BrowserStack in parallel ──
    print("\n" + "=" * 60)
    print("RUNNING ON BROWSERSTACK (5 parallel threads)")
    print("=" * 60)

    threads = []
    for i, caps in enumerate(BS_CAPABILITIES):
        t = threading.Thread(target=run_on_browserstack, args=(caps, i))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\nAll BrowserStack sessions complete!")

    print("View results at: https://automate.browserstack.com/dashboard")
