import os
import sqlite3
import psycopg2
from psycopg2.extras import DictCursor, execute_values
from dotenv import load_dotenv

DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "module1-introduction-to-sql", "rpg_db.sqlite3")
connection = sqlite3.connect(DB_FILEPATH)
connection.row_factory = sqlite3.Row
# print("CONNECTION:", connection)

cursor_sqlite = connection.cursor()
# print("CURSOR", cursor_sqlite)

load_dotenv()  # reads contents of the .env file and adds them to the environment

DB_POSTGRES_NAME = os.getenv("DB_POSTGRES_NAME", default="OOPS")
DB_POSTGRES_USER = os.getenv("DB_POSTGRES_USER", default="OOPS")
DB_POSTGRES_PASSWORD = os.getenv("DB_POSTGRES_PASSWORD", default="OOPS")
DB_POSTGRES_HOST = os.getenv("DB_POSTGRES_HOST", default="OOPS")

## Connect to ElephantSQL-hosted PostgreSQL
connection2 = psycopg2.connect(dbname=DB_POSTGRES_NAME, user=DB_POSTGRES_USER, password=DB_POSTGRES_PASSWORD, host=DB_POSTGRES_HOST)
# print("connection", connection2)

# cursor_pstgr = connection2.cursor() A "cursor", a structure to iterate over db records to perform queries
cursor_pstgr = connection2.cursor(cursor_factory=DictCursor) # to use data as dictionary representation instead of tuples
# print("cursor", cursor_pstgr)


tab_names=['armory%', 'character%'] 

tabnames=[]
for t in tab_names:
    cursor_sqlite.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%s'" % t)
    get_tab = cursor_sqlite.fetchall()
    for item in get_tab:
        tabnames.append(item[0])

tabnames.sort()

# tabnames = ['armory_item', 'armory_weapon', 'charactercreator_character', 'charactercreator_character_inventory', 
#             'charactercreator_cleric', 'charactercreator_fighter', 'charactercreator_mage', 'charactercreator_necromancer', 
#             'charactercreator_thief']

# Insert other tables
# other_tables = ["auth%", "django%", "sqlite%"]
other_tables = ['auth_user','auth_group', 'django_content_type', 'auth_permission', 'auth_group_permissions', 'auth_user_groups', 
                'auth_user_user_permissions', 'django_migrations', 'django_admin_log', 
                'django_session']

tabnames = tabnames + other_tables

for table in tabnames:
    # prepare queries and data from sqlite3
    cursor_sqlite.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name = ?;", (table,))
    create = cursor_sqlite.fetchone()[0]
    create = create.replace("AUTOINCREMENT", "").replace("integer NOT NULL", "SERIAL").replace("bool", "integer").replace("datetime", "timestamp").replace("unsigned", "");
    cursor_sqlite.execute("SELECT * FROM %s;" %table)
    rows=cursor_sqlite.fetchall()
    if len(rows) > 0:
        colcount=len(rows[0])
        pholder='%s,'*colcount
        newholder=pholder[:-1]
        # create tables in postgres and insert data 
        cursor_pstgr.execute("DROP TABLE IF EXISTS %s CASCADE;" %table)  # droping if exists (to run code multiple times)
        cursor_pstgr.execute(create)
        cursor_pstgr.executemany("INSERT INTO %s VALUES (%s);" % (table, newholder),rows)
        # save transaction
        connection2.commit()
        print('Created', table)
    else:
        cursor_pstgr.execute("DROP TABLE IF EXISTS %s CASCADE;" %table)   # droping if exists (to run code multiple times)
        cursor_pstgr.execute(create)
        connection2.commit()
        print('Created', table)    

# close connections
cursor_sqlite.close()
connection.close()
cursor_pstgr.close()
connection2.close()
