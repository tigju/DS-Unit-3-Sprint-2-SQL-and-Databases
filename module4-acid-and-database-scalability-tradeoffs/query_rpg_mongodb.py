import os
from dotenv import load_dotenv
import pymongo
import pprint


load_dotenv()  # reads contents of the .env file and adds them to the environment

MONGO_PASS = os.getenv("MONGO_PASS", default="OOPS")
MONGO_USER = os.getenv("MONGO_USER", default="OOPS")
# connect to mongodb 
client = pymongo.MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0-74vor.mongodb.net/test?retryWrites=true&w=majority")
rpg_db = client.rpg

# collection = rpg_db.test
# result = collection.insert_one({'stringy key': [2, 'thing', 3]})
# print(collection.find_one({'stringy key': [2, 'thing', 3]}))

queries = [
    # how many characters
    rpg_db.charactercreator_character.count_documents({}),
    # how many characters of each type
    rpg_db.charactercreator_cleric.count_documents({}),
    rpg_db.charactercreator_fighter.count_documents({}),
    rpg_db.charactercreator_mage.count_documents({}),
    rpg_db.charactercreator_necromancer.count_documents({}),
    rpg_db.charactercreator_thief.count_documents({}),
    # how many items
    rpg_db.armory_item.count_documents({}),
    # how many weapon items
    rpg_db.armory_weapon.count_documents({}),
    # how many items are not weapons
    
]

for query in queries:
    print("--------------")
    print(f"QUERY: '{query}'")

# quer = rpg_db.armory_item.aggregate([{
#     "$lookup":
#      {
#        "from": "armory_weapon",
#     #    "localField": "item_id",
#     #    "foreignField": "item_ptr_id",
#        "as": "common",
#        "pipeline": [{"$match": { "item_id": {"$ne": "item_ptr_id"}}}]
#      }
# }])




# query = rpg_db.armory_weapon.aggregate([{
#     "$lookup":
#         {
#         "from": "armory_item",
#         # "let": { "item_id": "$item_id"},
#         "pipeline": [
#             { "$match":
#                 { "$expr":
#                     { "item_id": {"$ne": ["item_ptr_id", "item_ptr_id"]}}
#                 }
#             },
#             { "$project": { "item_id": 3 } }
#         ],
#         "as": "data"
#     }
# }])

# print(query)

# for q in query:
#     print("--------------")
#     pprint.pprint(q)