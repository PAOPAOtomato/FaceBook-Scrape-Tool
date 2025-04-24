import openai
import re
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd

### Set API Key
openai.api_key = "sk-" ### hide for security reason

# --- Load cookies ---
with open("facebook_cookies.json", "r") as f:
    cookies = json.load(f)

# --- Setup Selenium ---
options = Options()
options.add_argument("--user-agent=Mozilla/5.0")
driver = webdriver.Chrome(service=Service(), options=options)
driver.get("https://www.facebook.com/")

# Add cookies
for cookie in cookies:
    if 'sameSite' in cookie:
        del cookie['sameSite']
    driver.add_cookie(cookie)

# Navigate to group search
search_url = "https://www.facebook.com/groups/589722428637008/search/?q=studio"
driver.get(search_url)
time.sleep(10)

# Scroll to load more posts
for _ in range(6):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

posts = soup.find_all("div", string=True)

### 🧠 Use GPT to filter
def gpt_classify(post_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are helping filter sublet listings."},
                {"role": "user", "content": f"""Is this Facebook post offering a short-term rental (studio or 1b1b) in Sandy Springs or Buckhead between May and August? Only answer 'Yes' or 'No'.\n\n{post_text}"""}
            ],
            temperature=0,
        )
        answer = response['choices'][0]['message']['content'].strip().lower()
        return "yes" in answer
    except Exception as e:
        print("OpenAI API error:", e)
        return False

### Clean & Filter posts
results = []
for post in posts:
    text = post.get_text(separator=" ").strip()
    if 100 < len(text) < 1000:  # reasonable size
        if gpt_classify(text):
            results.append(text)

### Generate HTML summary
html_template = """
<html><head><title>GPT-Filtered Facebook Posts</title></head><body>
<h2>Relevant Facebook Posts (via GPT)</h2>{}</body></html>
"""

blocks = []
for i, text in enumerate(results):
    snippet = text[:300].replace("\n", " ")
    block = f"""<div style="margin:15px; padding:10px; border:1px solid gray;">
        <a href="https://www.facebook.com/groups/589722428637008/search/?q=studio" target="_blank"><strong>Post #{i+1}</strong></a>
        <p>{snippet}...</p></div>"""
    blocks.append(block)

with open("gpt_filtered_posts.html", "w", encoding="utf-8") as f:
    f.write(html_template.format("\n".join(blocks)))

print(f"✅ Found {len(results)} posts GPT marked as relevant. Open gpt_filtered_posts.html to view.")
