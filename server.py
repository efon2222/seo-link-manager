from flask import Flask, request, jsonify
import re

app = Flask(__name__)

INTERNAL_LINKS = {
    "ייעוץ שינה": "https://www.lotemlerner.com/sleep-consulting",
    "ייעוץ הנקה": "https://www.lotemlerner.com/breastfeeding-consulting",
    "הנקה בלילה": "https://www.lotemlerner.com/night-breastfeeding",
    "גמילה מהנקה": "https://www.lotemlerner.com/weaning-guide",
    "תזונת תינוקות": "https://www.lotemlerner.com/baby-nutrition",
    "קשיים בהנקה": "https://www.lotemlerner.com/breastfeeding-difficulties",
    "שינה של תינוקות": "https://www.lotemlerner.com/baby-sleep-tips"
}

EXTERNAL_SOURCES = {
    "הנקה בלילה": "https://pubmed.ncbi.nlm.nih.gov/?term=night+breastfeeding",
    "שינה של תינוקות": "https://www.sleepfoundation.org/baby-sleep",
    "תזונת תינוקות": "https://www.who.int/nutrition/topics/infantfeeding_recommendation/en/",
    "יתרונות חלב אם": "https://www.cdc.gov/breastfeeding/faq/index.htm"
}

def add_links(article_text):
    """ הוספת קישורים חיצוניים ופנימיים עם אפשרות לאישור ידני """
    suggested_links = []

    for keyword, link in INTERNAL_LINKS.items():
        if keyword in article_text:
            suggested_links.append((keyword, link, "פנימי"))

    for keyword, link in EXTERNAL_SOURCES.items():
        if keyword in article_text:
            suggested_links.append((keyword, link, "חיצוני"))

    return suggested_links

@app.route('/generate_links', methods=['POST'])
def generate_links():
    data = request.json
    article = data.get("article", "תוכן המאמר חסר")
    
    # מציע למשתמש קישורים ומבקש אישור
    suggested_links = add_links(article)

    return jsonify({"suggested_links": suggested_links})

@app.route('/apply_links', methods=['POST'])
def apply_links():
    data = request.json
    article = data.get("article", "תוכן המאמר חסר")
    approved_links = data.get("approved_links", [])

    for keyword, link, _ in approved_links:
        article = re.sub(rf"\b{keyword}\b", f'<a href="{link}">{keyword}</a>', article, flags=re.IGNORECASE)

    return jsonify({"article": article})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
