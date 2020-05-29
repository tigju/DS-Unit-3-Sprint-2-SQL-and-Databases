import os
import psycopg2
from psycopg2.extras import DictCursor, execute_values
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

queries = [
    "SELECT COUNT(DISTINCT id) as passengers, survived FROM titanic GROUP BY survived;",
    "SELECT COUNT(DISTINCT id) as passengers, pclass FROM titanic GROUP BY pclass;",
    "SELECT pclass, survived, COUNT(DISTINCT id) as passengers FROM titanic GROUP BY survived, pclass ORDER BY pclass;",
    "SELECT survived, AVG(age) as average_age FROM titanic GROUP BY survived;",
    "SELECT pclass, AVG(age) as average_age FROM titanic GROUP BY pclass;",
    "SELECT pclass, survived, AVG(fare) as average_fare FROM titanic GROUP BY pclass, survived ORDER BY pclass, survived;",
    "SELECT pclass, survived, AVG(siblings_spouses_aboard) as siblings_spouses FROM titanic WHERE siblings_spouses_aboard <> 0 GROUP BY pclass, survived ORDER BY pclass, survived",
    "SELECT pclass, survived, AVG(parents_children_aboard) as avg_parents_children FROM titanic WHERE parents_children_aboard <> 0 GROUP BY pclass, survived ORDER BY pclass, survived"
]

for query in queries:
    print("--------------")
    print(f"QUERY: '{query}'")
    cursor.execute(query)
    column_names = [desc[0] for desc in cursor.description]
    print(column_names)
    for row in cursor.fetchall():
        print(row)


