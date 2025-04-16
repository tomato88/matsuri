from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def scrape_walkerplus(city):
    url = f"https://www.walkerplus.com/event_list/{city}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    events = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for item in soup.select(".eventListItem"):
            title_tag = item.select_one(".eventTitle")
            date_tag = item.select_one(".eventDate")
            link_tag = item.select_one("a")
            if title_tag and date_tag and link_tag:
                events.append({
                    "title": title_tag.text.strip(),
                    "date": date_tag.text.strip(),
                    "link": "https://www.walkerplus.com" + link_tag["href"]
                })
    except Exception as e:
        print("Walkerplus Error:", e)
    return events

def scrape_jalan(city):
    url = f"https://www.jalan.net/event/evtSearch.do?areaCd=3&keyword={city}"
    headers = {"User-Agent": "Mozilla/5.0"}
    events = []
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for li in soup.select(".mB20 > ul > li"):
            title_tag = li.select_one("a")
            date_tag = li.find(string=re.compile("開催期間"))
            if title_tag and date_tag:
                events.append({
                    "title": title_tag.text.strip(),
                    "date": date_tag.strip(),
                    "link": "https://www.jalan.net" + title_tag["href"]
                })
    except Exception as e:
        print("Jalan Error:", e)
    return events

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    city = request.form.get("city")
    results = scrape_walkerplus(city) + scrape_jalan(city)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
