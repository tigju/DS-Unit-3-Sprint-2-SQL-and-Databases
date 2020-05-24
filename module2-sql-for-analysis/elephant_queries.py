import os
import json
import psycopg2
from psycopg2.extras import DictCursor, execute_values
from dotenv import load_dotenv
import pandas as pd


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
# cursor.execute('SELECT * from test_table;')
### Note - nothing happened yet! We need to actually *fetch* from the cursor
# result = cursor.fetchone()
# type(result) #> <class 'tuple'>
#> (1, 'A row name', None)
# result = cursor.fetchall()
# for row in result:
#     print('-----------')
#     print(type(row))
#     print(row)

#
# CREATE NEW TABLE
#

print("-------------------")
query = """
CREATE TABLE IF NOT EXISTS test_table2(
  id SERIAL PRIMARY KEY,
  name varchar(40) NOT NULL,
  data JSONB
);
"""
print("SQL:", query)
cursor.execute(query)

#
# INSERT SOME DATA
#

my_dict = { "a": 1, "b": ["dog", "cat", 42], "c": 'true' }

# insert one row at a time

# insertion_query = "INSERT INTO test_table2 (name, data) VALUES (%s, %s)"
# cursor.execute(insertion_query,
#  ('A rowwwww', 'null')
# )
# cursor.execute(insertion_query,
#  ('Another row, with JSONNNNN', json.dumps(my_dict))
# )

# h/t: https://stackoverflow.com/questions/8134602/psycopg2-insert-multiple-rows-with-one-query
# insertion_query = "INSERT INTO test_table2 (name, data) VALUES %s"
# execute_values(cursor, insertion_query, [
#  ('A rowwwww', 'null'),
#  ('Another row, with JSONNNNN', json.dumps(my_dict)),
#  ('Third row', "3")
# ]) # third param (data to insert) is a LIST OF TUPLES

#############################
df = pd.DataFrame([
  ['A rowwwww', 'null'],
  ['Another row, with JSONNNNN', json.dumps(my_dict)],
  ['Third row', "null"],
  ["Pandas Row", "null"]
])
# convert data to a list of tuples before inserting 

records = df.to_dict("records") #> [{0: 'A rowwwww', 1: 'null'}, {0: 'Another row, with JSONNNNN', 1: '{"a": 1, "b": ["dog", "cat", 42], "c": "true"}'}, {0: 'Third row', 1: '3'}, {0: 'Pandas Row', 1: 'YOOO!'}]
list_of_tuples = [(r[0], r[1]) for r in records]

insertion_query = "INSERT INTO test_table2 (name, data) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples)
##############################
#
# QUERY THE TABLE
#

print("-------------------")
query = "SELECT * FROM test_table2;"
print("SQL:", query)
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()

cursor.close()
connection.close()