import yfinance as yf
import feedparser
from datetime import datetime
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.message import EmailMessage
import os

# ---------------------------
# DATE
# ---------------------------

today = datetime.now().strftime("%d %B %Y")

# ---------------------------
# FETCH INDIA BUSINESS NEWS
# ---------------------------

india_feed = feedparser.parse(
    "https://news.google.com/rss/search?q=india+business&hl=en-IN&gl=IN&ceid=IN:en"
)

india_news = india_feed.entries[:5]

# ---------------------------
# FETCH GLOBAL BUSINESS NEWS
# ---------------------------

global_feed = feedparser.parse(
    "https://news.google.com/rss/search?q=global+business&hl=en-US&gl=US&ceid=US:en"
)

global_news = global_feed.entries[:5]

# ---------------------------
# MARKET DATA
# ---------------------------

nifty = yf.Ticker("^NSEI").history(period="2d")
sensex = yf.Ticker("^BSESN").history(period="2d")

nifty_price = round(nifty["Close"].iloc[-1],2)
sensex_price = round(sensex["Close"].iloc[-1],2)

nifty_change = round(((nifty["Close"].iloc[-1] - nifty["Close"].iloc[-2]) / nifty["Close"].iloc[-2]) * 100,2)
sensex_change = round(((sensex["Close"].iloc[-1] - sensex["Close"].iloc[-2]) / sensex["Close"].iloc[-2]) * 100,2)

# ---------------------------
# GAINERS / LOSERS (NIFTY)
# ---------------------------

nifty_stocks = ["RELIANCE.NS","TCS.NS","INFY.NS","ITC.NS","HDFCBANK.NS",
                "ICICIBANK.NS","SBIN.NS","LT.NS","BHARTIARTL.NS","HCLTECH.NS"]

data = yf.download(nifty_stocks, period="2d")["Close"]

changes = {}

for stock in nifty_stocks:
    change = ((data[stock].iloc[-1] - data[stock].iloc[-2]) / data[stock].iloc[-2]) * 100
    changes[stock] = change

sorted_stocks = sorted(changes.items(), key=lambda x: x[1], reverse=True)

gainers = sorted_stocks[:5]
losers = sorted_stocks[-5:]

# ---------------------------
# MARKET COMMENTARY
# ---------------------------

commentary = "Markets remained volatile due to global economic uncertainty and rising crude oil prices. Investors may remain cautious in the next session while tracking global market cues and inflation data."

# ---------------------------
# GITA THOUGHT
# ---------------------------

gita = [
("कर्मण्येवाधिकारस्ते मा फलेषु कदाचन",
"You have the right to perform your duties but not to the fruits of your actions."),
("योगः कर्मसु कौशलम्",
"Excellence in action is yoga."),
("उद्धरेदात्मनात्मानं",
"Lift yourself through self discipline and wisdom.")
]

gita_shloka, gita_meaning = random.choice(gita)

# ---------------------------
# CREATE PDF
# ---------------------------

filename = "Daily_Finance_Report.pdf"

c = canvas.Canvas(filename, pagesize=letter)
width, height = letter

y = height - 40

c.setFont("Helvetica-Bold",16)
c.drawString(50,y,"Daily India & Global Business Brief")

y -= 25
c.setFont("Helvetica",10)
c.drawString(50,y,f"Date: {today}")

y -= 40

# INDIA NEWS
c.setFont("Helvetica-Bold",12)
c.drawString(50,y,"Top 5 India Business News")

y -= 20
c.setFont("Helvetica",10)

for i,news in enumerate(india_news,1):

    c.drawString(50,y,f"{i}. {news.title[:90]}")
    y -= 15
    c.drawString(60,y,"Short summary: Key developments impacting Indian economy and business environment.")
    y -= 25

# GLOBAL NEWS
c.setFont("Helvetica-Bold",12)
c.drawString(50,y,"Top 5 Global Business News")

y -= 20
c.setFont("Helvetica",10)

for i,news in enumerate(global_news,1):

    c.drawString(50,y,f"{i}. {news.title[:90]}")
    y -= 15
    c.drawString(60,y,"Short summary: Major global developments influencing financial markets.")
    y -= 25

# MARKET UPDATE
c.setFont("Helvetica-Bold",12)
c.drawString(50,y,"Market Update")

y -= 20
c.setFont("Helvetica",10)

c.drawString(50,y,f"Nifty: {nifty_price} ({nifty_change}%)")
y -= 15
c.drawString(50,y,f"Sensex: {sensex_price} ({sensex_change}%)")

y -= 25
c.drawString(50,y,"Market Commentary:")
y -= 15
c.drawString(60,y,commentary)

y -= 30

# GAINERS
c.setFont("Helvetica-Bold",12)
c.drawString(50,y,"Top 5 Gainers")

y -= 20
c.setFont("Helvetica",10)

for stock,change in gainers:
    c.drawString(50,y,f"{stock} : {round(change,2)}%")
    y -= 15

y -= 20

# LOSERS
c.setFont("Helvetica-Bold",12)
c.drawString(50,y,"Top 5 Losers")

y -= 20
c.setFont("Helvetica",10)

for stock,change in losers:
    c.drawString(50,y,f"{stock} : {round(change,2)}%")
    y -= 15

y -= 30

# GITA BOX
c.setFont("Helvetica-Bold",12)
c.drawString(50,y,"Bhagavad Gita Thought")

y -= 20
c.setFont("Helvetica",10)

c.drawString(50,y,gita_shloka)
y -= 15
c.drawString(50,y,gita_meaning)

c.save()

# ---------------------------
# EMAIL
# ---------------------------

EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

msg = EmailMessage()
msg["Subject"] = f"Daily Finance Update - {today}"
msg["From"] = EMAIL_ADDRESS
msg["To"] = EMAIL_ADDRESS
msg.set_content("Attached is your daily finance report.")

with open(filename,"rb") as f:
    msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=filename)

with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
    smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
    smtp.send_message(msg)

print("Report generated and email sent.")
