# Install libraries (only needed in Colab testing)
# !pip install yfinance feedparser

import yfinance as yf
import feedparser
import random
from datetime import datetime

# ----------------------------
# 1. Fetch Business News
# ----------------------------

rss_url = "https://news.google.com/rss/search?q=india+business"
feed = feedparser.parse(rss_url)

news_items = []
for entry in feed.entries[:5]:
    summary = entry.summary if "summary" in entry else "Summary not available."
    news_items.append({
        "title": entry.title,
        "summary": summary
    })

# ----------------------------
# 2. Fetch Market Data + Commentary Logic
# ----------------------------

def get_market_data(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="2d")
    today_close = hist["Close"].iloc[-1]
    yesterday_close = hist["Close"].iloc[-2]
    change = today_close - yesterday_close
    pct_change = (change / yesterday_close) * 100
    return today_close, pct_change

nifty_price, nifty_pct = get_market_data("^NSEI")
sensex_price, sensex_pct = get_market_data("^BSESN")

def market_commentary(index_name, pct):
    if pct > 1:
        return f"{index_name} showed strong bullish momentum with gains above 1%, indicating positive investor sentiment."
    elif 0 < pct <= 1:
        return f"{index_name} remained slightly positive, showing cautious optimism in the markets."
    elif -1 <= pct <= 0:
        return f"{index_name} closed marginally lower, reflecting mild profit booking."
    else:
        return f"{index_name} declined significantly, indicating bearish pressure or macro concerns."

nifty_comment = market_commentary("Nifty", nifty_pct)
sensex_comment = market_commentary("Sensex", sensex_pct)

# ----------------------------
# 3. Gita Shloka
# ----------------------------

gita_shlokas = [
    {
        "shloka": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन",
        "meaning": "You have the right to perform your duties, but not the fruits of your actions."
    },
    {
        "shloka": "योगः कर्मसु कौशलम्",
        "meaning": "Excellence in action is yoga."
    }
]

today_shloka = random.choice(gita_shlokas)

# ----------------------------
# 4. Smart Finance Insight Based on Market
# ----------------------------

if nifty_pct > 0:
    finance_insight = "Market strength reminds investors that disciplined long-term investing rewards patience."
else:
    finance_insight = "Market volatility is an opportunity for disciplined investors to accumulate quality assets at better valuations."

# ----------------------------
# 5. Format Blog Output
# ----------------------------

today_date = datetime.now().strftime("%d %B %Y")

blog_content = f"""
📊 Daily India Business Update – {today_date}

📰 Top 5 Business News

"""

for i, news in enumerate(news_items, 1):
    blog_content += f"{i}. {news['title']}\n"
    blog_content += f"   ➤ {news['summary'][:250]}...\n\n"

blog_content += f"""
📈 Market Update

Nifty: {round(nifty_price,2)} ({round(nifty_pct,2)}%)
{nifty_comment}

Sensex: {round(sensex_price,2)} ({round(sensex_pct,2)}%)
{sensex_comment}

💡 Omkar’s Finance Insight
{finance_insight}

📖 Bhagavad Gita Thought
Shloka: {today_shloka['shloka']}
Meaning: {today_shloka['meaning']}

---
Prepared by Omkar Finance AI Assistant
"""

print(blog_content)
