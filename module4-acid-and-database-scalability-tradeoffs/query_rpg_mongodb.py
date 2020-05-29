import os
from dotenv import load_dotenv
import pymongo


load_dotenv()  # reads contents of the .env file and adds them to the environment

MONGO_PASS = os.getenv("MONGO_PASS", default="OOPS")

# connect to mongodb 
client = pymongo.MongoClient(f"mongodb+srv://iuliiastanina:{MONGO_PASS}@cluster0-74vor.mongodb.net/test?retryWrites=true&w=majority")
rpg_db = client.rpg

collection = rpg_db.test
# result = collection.insert_one({'stringy key': [2, 'thing', 3]})
# print(collection.find_one({'stringy key': [2, 'thing', 3]}))

queries = [
    collection.find_one({'stringy key': [2, 'thing', 3]}),
    collection.find_one({'stringy key': [2, 'thing', 3]})
]

for query in queries:
    print("--------------")
    print(f"QUERY: '{query}'")
