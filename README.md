# Facebook Sublet Finder with GPT

This project helps you automatically filter sublet listings (e.g., studio or 1b1b) from a Facebook housing group based on your specific location and date criteria. It mimics human judgment using OpenAI's GPT-3.5 model.

---

## What It Does

- Logs into Facebook using your saved session cookies
- Scrapes posts from a Facebook group (e.g., Atlanta housing groups)
- Uses GPT-3.5 to determine if each post:
  - Offers a short-term rental
  - Is in Sandy Springs or Buckhead
  - Falls between May and August
- Outputs relevant listings into a formatted HTML file

---

## Why GPT?

Traditional keyword filters miss posts due to vague or varied wording. GPT understands context, so posts like:

> *“Available from late May — 1B in Buckhead, walkable to Marta, pet-friendly!”*

...are correctly included even without strict keyword matches.

---

## Requirements

You'll also need:

- Google Chrome installed  
- `chromedriver` in your `PATH` (or handled via `webdriver-manager`)

---
## How to Use

## Facebook Session Setup

1. Install [CopyCookies]([https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg](https://chromewebstore.google.com/detail/copy-cookies/jcbpglbplpblnagieibnemmkiamekcdg))
2. Log in to Facebook
3. Navigate to your target housing group
4. Export cookies as `.json`
5. Save them in your project as `facebook_cookies.json`

---

## OpenAI Setup
1. Copy your API key and add it in your script:

```python
openai.api_key = "sk-..."  # ← Insert your actual key
```

## Usage

Run the script from terminal:

```bash
python facebook_sublet_filter.py
```

Then open `gpt_filtered_posts.html` in your browser to see matched listings.

---

## GPT Prompt Example

Each post is classified using this prompt:

> Is this Facebook post offering a short-term rental (studio or 1b1b) in Sandy Springs or Buckhead between May and August?  
> Only answer "Yes" or "No".

---

## Output

- `gpt_filtered_posts.html`: A summary page of all matched posts, each with a preview and link to the group search page  
- Can be extended to `.csv`, `.json`, or automated alerts

---
