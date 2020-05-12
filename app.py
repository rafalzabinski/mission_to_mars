from flask import Flask
from flask import render_template
import pymongo
import mission_to_mars
from flask import jsonify

app = Flask(__name__)
conn = 'mongodb://localhost:27017/mission_to_mars'
client = pymongo.MongoClient(conn)

db = client['mars']
db.mars.drop()
collection = db['mars_collection']


@app.route("/")
def index():
    mars = client.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape 
@app.route("/scrape")
def scrape():
    mars = client.db.mars
    mars_data = mission_to_mars.scrape()
    mars.insert(mars_data)
    #mars.update({}, mars_data)
    return ("Scrape is complete! Go to /")

if __name__ == '__main__':
    app.run(debug=True)