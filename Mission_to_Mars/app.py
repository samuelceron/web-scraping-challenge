from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    db.mars.update({}, mars_dict, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)