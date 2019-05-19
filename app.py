from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# mymongo document https://flask-pymongo.readthedocs.io/en/latest/
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection # access to mars_app db by specifying 'mongo.db'
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Query
    mars_info = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scraper():
    
    # Run the scrape function and save the results to a variable
    scraped = scrape_mars.scrape()

    # Update the Mongo db(mars_app) at collection 'mars_data' using update and upsert=True
    mars_collection = mongo.db.mars_data
    mars_collection.update({}, scraped, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)