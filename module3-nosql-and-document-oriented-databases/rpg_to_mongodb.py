import os
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor, execute_values
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd
import pymongo

load_dotenv()  # reads contents of the .env file and adds them to the environment

DB_POSTGRES_NAME = os.getenv("DB_POSTGRES_NAME", default="OOPS")
DB_POSTGRES_USER = os.getenv("DB_POSTGRES_USER", default="OOPS")
DB_POSTGRES_PASSWORD = os.getenv("DB_POSTGRES_PASSWORD", default="OOPS")
DB_POSTGRES_HOST = os.getenv("DB_POSTGRES_HOST", default="OOPS")

MONGO_PASS = os.getenv("MONGO_PASS", default="OOPS")

# Connect to ElephantSQL-hosted PostgreSQL
connection = psycopg2.connect(dbname=DB_POSTGRES_NAME, user=DB_POSTGRES_USER, password=DB_POSTGRES_PASSWORD, host=DB_POSTGRES_HOST)
print("connection", connection)

# cursor = connection.cursor() A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor(cursor_factory=DictCursor) # to use data as dictionary representation instead of tuples
print("cursor", cursor)


client = pymongo.MongoClient(f"mongodb+srv://iuliiastanina:{MONGO_PASS}@cluster0-74vor.mongodb.net/test?retryWrites=true&w=majority")
rpg_db = client.rpg

engine = create_engine('postgres://vvjcyugm:sDTtNJiTs1ebGESvJdEvK_f9v9I9ctmK@ruby.db.elephantsql.com:5432/vvjcyugm', echo=False)

tabnames = ['armory_item', 'armory_weapon', 'charactercreator_character', 'charactercreator_character_inventory', 
             'charactercreator_cleric', 'charactercreator_fighter', 'charactercreator_mage', 'charactercreator_necromancer', 
             'charactercreator_thief', 'auth_user','auth_group', 'django_content_type', 'auth_permission', 'auth_group_permissions', 'auth_user_groups', 
                'auth_user_user_permissions', 'django_migrations', 'django_admin_log', 
                'django_session']

dict_of_tables = {}
for table in tabnames:
    query = """
            SELECT * 
            FROM %s
            """ %table
    dict_of_tables[table] = pd.read_sql_query(query, engine)


# print(type(dict_of_tables['armory_item'].to_dict()))
# result = rpg_db.insert_one(dict_of_tables['armory_item'].to_dict())
# print(result)








