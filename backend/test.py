import urllib.parse
import pymongo


#Insert into status collection in mongodb with pymongo
def insert_into_mongodb(status):
    username = "midhun"
    password = "heyphil"
    uri = f"mongodb+srv://{urllib.parse.quote_plus(username)}:{urllib.parse.quote_plus(password)}@pvm.54wtzjn.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri, tlsAllowInvalidCertificates=True)
    db = client["pvm"]
    collection = db["status"]
    collection.insert_one(status)
    return True


#Test the insert into mongodb function
print(insert_into_mongodb({"project_id": "1234", "project_status": "In Progress"}))
