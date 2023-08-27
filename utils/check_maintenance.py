import flask_pymongo
from config import mongo_uri
mongodb_client = flask_pymongo.pymongo.MongoClient(mongo_uri)
mydb = mongodb_client['jellyfishhost']

def check_maintenance():
    siteCollections = mydb['sitesettings']
    data = siteCollections.find_one({"system": "yes"})
    isMaintenance = data.get('maintenance')
    if isMaintenance == "yes":
        return "yes"
    else:
        return "no"