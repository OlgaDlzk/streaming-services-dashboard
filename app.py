from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
import json
from bson import json_util
from bson.json_util import dumps
# import create_mongodb
import pymongo
import pandas as pd
import json

def create_db():

    # connection using pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017")

    # read in csv file as dataframe
    df_horizontal = pd.read_csv("static/etl/csv/complete_data/complete_horizontal.csv")
    df_vertical = pd.read_csv("static/etl/csv/complete_data/complete_vertical.csv")

    # map index to string for bson compatibility
    df_horizontal.index = df_horizontal.index.map(str)
    df_vertical.index = df_vertical.index.map(str)

    # Nan to None for proper JSON specs
    df_horizontal = df_horizontal.where(df_horizontal.notna(), None)
    df_vertical = df_vertical.where(df_vertical.notna(), None)

    # new variable of df that converts data to dictionary
    # where each row is its own dictionary (orient="records")
    # list of dictionaries
    data_horizontal = df_horizontal.to_dict(orient="index")
    data_vertical = df_vertical.to_dict(orient="index")

    # connect to db, one will be created if it does not exist yet
    db = client["streamTest"]

    # connect to collection and drop if it exists
    mycol = db["streamData"]
    mycol.drop()

    horCol = db["streamHorizontal"]
    horCol.drop()

    vertCol = db["streamVertical"]
    vertCol.drop()

    sunCol = db["streamSunburst"]
    sunCol.drop()

    # create streamData collection and insert data
    # db.streamData.insert_many(data)
    db.streamHorizontal.insert_one(data_horizontal)

    db.streamVertical.insert_one(data_vertical)

     #open sunburst json file
    with open("static/etl/json/sunburst_data.json") as file:
        file_data = json.load(file)

    # insert into streamSunburst collection
    if isinstance(file_data, list):
        db.streamSunburst.insert_many(file_data)
    else:
        db.streamSunburst.insert_one(file_data)

# create instance of Flask class
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/streamTest"
mongo = PyMongo(app)


# define how we get to page with app.route
@app.route("/")
# what will be displayed on pg wrapped in this function
def home():
    create_db()
    # first document in the collection
    # first_record = mongo.db.streamHorizontal.find_one()

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
    mongo_horizontal = mongo.db.streamHorizontal.find()
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
    mongo_vertical = mongo.db.streamVertical.find()
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
    mongo_vertical = mongo.db.streamSunburst.find({}, {"_id": 0})
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
