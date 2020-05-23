import pandas as pd
import os
import sqlite3
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

my_df = pd.read_csv("../buddymove_holidayiq.csv")
#print(my_df.head(3))

my_df.to_sql('buddymove_holidayiq', con=engine)

DB_FILEPATH = os.path.join(os.path.dirname(
    __file__), "..", "buddymove_holidayiq.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
connection.row_factory = sqlite3.Row
print("CONNECTION:", connection)

cursor = connection.cursor()
# print("CURSOR", cursor)

query1 = "SELECT COUNT(DISTINCT 'User ID') AS number_of_rows"
result1 = cursor.execute(query1).fetchall()
print("Number of rows: ", result1[0][0])
