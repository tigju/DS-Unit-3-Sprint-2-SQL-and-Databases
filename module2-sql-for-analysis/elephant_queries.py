import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv


load_dotenv()  # reads contents of the .env file and adds them to the environment

DB_NAME = os.getenv("DB_NAME", default="OOPS")
DB_USER = os.getenv("DB_USER", default="OOPS")
DB_PASSWORD = os.getenv("DB_PASSWORD", default="OOPS")
DB_HOST = os.getenv("DB_HOST", default="OOPS")

### Connect to ElephantSQL-hosted PostgreSQL
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

print("connection", connection)

### A "cursor", a structure to iterate over db records to perform queries
# cursor = connection.cursor()
cursor = connection.cursor(cursor_factory=DictCursor) # to use data as dictionary representation instead of tuples
print("cursor", cursor)


### An example query
cursor.execute('SELECT * from test_table;')
### Note - nothing happened yet! We need to actually *fetch* from the cursor
# result = cursor.fetchone()
# type(result) #> <class 'tuple'>
#> (1, 'A row name', None)
result = cursor.fetchall()
for row in result:
    print('-----------')
    print(type(row))
    print(row)
