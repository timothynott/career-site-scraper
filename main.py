import os

from flask import Flask
from scrapers.scraper_runner import ScraperRunner

app = Flask(__name__)


@app.put("/")
def do_the_thing():
    scraper = ScraperRunner()
    scraper.run()
    return ('', 204)


if __name__ == "__main__":
    app.run(debug=False, host=os.environ.get("HOST", "0.0.0.0"),
            port=int(os.environ.get("PORT", 8080)))
