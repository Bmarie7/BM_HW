from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo

# edited by JA
import pymongo

import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars

@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars = db.mars_app
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
