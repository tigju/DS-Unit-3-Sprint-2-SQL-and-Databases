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

titanic_df = pd.read_csv("./titanic.csv")


# create enumerated data
create_types_query = """
                    CREATE TYPE sex AS ENUM ('male', 'female');
                    """
print("Types:", create_types_query)
cursor.execute(create_types_query)

create_table_query = """
                    CREATE TABLE IF NOT EXISTS titanic(
                    id SERIAL PRIMARY KEY,
                    survived INTEGER CHECK (survived>=0 AND survived<=1),
                    pclass INTEGER CHECK (pclass>=1 AND pclass<=3),
                    name varchar(120) NOT NULL,
                    sex sex,
                    age INTEGER,
                    siblings_spouses_aboard INTEGER,
                    parents_children_aboard INTEGER,
                    fare DECIMAL
 );
"""
print("SQL:", create_table_query)
cursor.execute(create_table_query)


# convert df_titanic to a list of tuples before inserting 
records = titanic_df.to_dict("records") #> [{0: 'A rowwwww', 1: 'null'}, {0: 'Another row, with JSONNNNN', 1: '{"a": 1, "b": ["dog", "cat", 42], "c": "true"}'}, {0: 'Third row', 1: '3'}, {0: 'Pandas Row', 1: 'YOOO!'}]
list_of_tuples = [(r['Survived'], r['Pclass'], r['Name'], r['Sex'], r['Age'], r['Siblings/Spouses Aboard'], r['Parents/Children Aboard'], r['Fare']) for r in records]

insertion_query = "INSERT INTO titanic (survived, pclass, name, sex, age, siblings_spouses_aboard, parents_children_aboard, fare) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples)

#
# QUERY THE TABLE
#

print("-------------------")
query = "SELECT * FROM titanic;"
print("SQL:", query)
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()

cursor.close()
connection.close()

# exploration of titanic data

query1 = """
        SELECT  COUNT(id) AS num_people,
		AVG(age) AS avg_age,
	    AVG(fare) AS avg_fare,
	    AVG(survived)*100 AS survival_percent
        FROM titanic;
        """
print("Query 1:", query1)
cursor.execute(query1)
for row in cursor.fetchall():
    print(f"people count: {row['num_people']}, average age: {row['avg_age']}, average fare: {row['avg_fare']}, percent of survivals: {row['survival_percent']}")

query2 = """
        SELECT pclass, survived, sex, 
	    COUNT(id) AS num_people
        FROM titanic
        GROUP BY pclass, survived, sex
        ORDER BY pclass;
        """
print("Query 2:", query2)
cursor.execute(query2)
for row in cursor.fetchall():
    print(f"Pclass: {row['pclass']}, survived: {row['survived']}, sex: {row['sex']}, people_number: {row['num_people']}")