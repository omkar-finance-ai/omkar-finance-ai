import yfinance as yf
import feedparser
import random
from datetime import datetime
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

# ----------------------------
# 1. Fetch Business News
# ----------------------------
rss_url = "https://news.google.com/rss/search?q=india+business"
feed = feedparser.parse(rss_url)

news_items = []
for entry in feed.entries[:5]:
    summary = entry.summary if "summary" in entry else ""
    news_items.append({
        "title": entry.title,
        "summary": summary[:250]
    })

# ----------------------------
# 2. Market Data
# ----------------------------
def get_market_data(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="2d")
    today_close = hist["Close"].iloc[-1]
    yesterday_close = hist["Close"].iloc[-2]
    pct_change = ((today_close - yesterday_close) / yesterday_close) * 100
    return today_close, pct_change

nifty_price, nifty_pct = get_market_data("^NSEI")
sensex_price, sensex_pct = get_market_data("^BSESN")

# ----------------------------
# 3. Gita
# ----------------------------
gita = {
    "shloka": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन",
    "meaning": "You have the right to perform your duties, but not the fruits of your actions."
}

finance_insight = "Market discipline and long-term investing create sustainable wealth."

# ----------------------------
# 4. Create Blog Content
# ----------------------------
today_date = datetime.now().strftime("%d %B %Y")

blog_content = f"Daily India Business Update – {today_date}\n\n"

blog_content += "Top 5 Business News\n\n"

for i, news in enumerate(news_items, 1):
    blog_content += f"{i}. {news['title']}\n"
    blog_content += f"{news['summary']}\n\n"

blog_content += f"\nMarket Update\n"
blog_content += f"Nifty: {round(nifty_price,2)} ({round(nifty_pct,2)}%)\n"
blog_content += f"Sensex: {round(sensex_price,2)} ({round(sensex_pct,2)}%)\n\n"

blog_content += f"Finance Insight:\n{finance_insight}\n\n"

blog_content += f"Gita Thought:\n{gita['shloka']}\nMeaning: {gita['meaning']}\n"

# ----------------------------
# 5. Convert to PDF
# ----------------------------
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=11)

safe_text = blog_content.encode("latin-1", "replace").decode("latin-1")

for line in safe_text.split("\n"):
    pdf.multi_cell(0, 8, line)

filename = f"Daily_Update_{today_date}.pdf"
pdf.output(filename)

# ----------------------------
# 6. Send Email
# ----------------------------
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

msg = EmailMessage()
msg["Subject"] = f"Daily Finance Update - {today_date}"
msg["From"] = EMAIL_ADDRESS
msg["To"] = EMAIL_ADDRESS
msg.set_content("Attached is your daily finance blog PDF.")

with open(filename, "rb") as f:
    file_data = f.read()
    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=filename)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)

print("Email sent successfully!")
