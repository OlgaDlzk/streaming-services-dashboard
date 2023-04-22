from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
import create_mongodb
from dotenv import load_dotenv
import os 
from pymongo import MongoClient
from config import password

# load_dotenv() # use dotenv to hide sensitive credential as environment variables

DATABASE_URL= f'mongodb+srv://loooret:{password}@cluster0.zf9dnan.mongodb.net/?retryWrites=true&w=majority' # get connection url from environment
# DATABASE_URL=f'mongodb+srv://loooret:{os.getenv("[DATABASE_URL]")}'\
#               '@cluster0.zf9dnan.mongodb.net/?retryWrites=true&w=majority' # get connection url from environment

# client=pymongo.MongoClient(DATABASE_URL) # establish connection with database

# mongo_db=client.db

# create instance of Flask class
app = Flask(__name__)
# mongo_url = "mongodb://localhost:27017"
mongo_url = DATABASE_URL

# app.config["MONGO_URI"] = mongo_url + "/streamTest"
app.config["MONGO_URI"] = mongo_url 
# mongo = PyMongo(app)

cluster = MongoClient(DATABASE_URL)
db = cluster["streamTest"]
# define how we get to page with app.route
@app.route("/")
# what will be displayed on pg wrapped in this function
def home():
    # create_mongodb.create_db(mongo_url)

    # first document in the collection
    # first_record = mongo.db.streamHorizontal.find_one()
    # print(first_record)

    return render_template("index.html")


# after the source file is where the {{variable}} from the html is being set to


@app.route("/wheel")
def wheel():
    return render_template("wheel.html")


@app.route("/team")
def team():
    return render_template("team.html")


@app.route("/get_horizontal")
def get_horizontal():
    # variable to find all data in streamData collection
    # mongo_horizontal = mongo.db.streamHorizontal.find()     #######################
    mongo_horizontal = db.streamHorizontal.find()     #######################
    # empty list to be transformed into json object
    json_horizontal = {}
    for all in mongo_horizontal:
        json_horizontal.update(all)
    # remove mongo created id
    del json_horizontal["_id"]
    # converting mongo encoding to json
    json_horizontal = json.dumps(json_horizontal, default=json_util.default)
    return json_horizontal


@app.route("/get_vertical")
def get_vertical():
    # variable to find all data in streamData collection
    # mongo_vertical = mongo.db.streamVertical.find()         ###############
    mongo_vertical = db.streamVertical.find()         ###############
    # empty list to be transformed into json object
    json_vertical = {}
    for all in mongo_vertical:
        json_vertical.update(all)
    # remove mongo created id
    del json_vertical["_id"]
    # converting mongo encoding to json
    json_vertical = json.dumps(json_vertical, default=json_util.default)
    return json_vertical


@app.route("/get_sunburst")
def get_sunburst():
    # variable to find all data in streamData collection
    # mongo_vertical = mongo.db.streamSunburst.find({}, {"_id": 0})   ######################
    mongo_vertical = db.streamSunburst.find({}, {"_id": 0})   ######################
    # empty list to be transformed into json object
    json_sunburst = []
    for all in mongo_vertical:
        json_sunburst.append(all)
    # remove mongo created id
    # del json_vertical["_id"]
    # converting mongo encoding to json
    json_sunburst = json.dumps(json_sunburst, default=json_util.default)
    return json_sunburst


# run webpage
# set debug to True if you want server to auto reload code changes
# and will show interactive debugger in browser if error occurs
if __name__ == "__main__":
    app.run(debug=True)
