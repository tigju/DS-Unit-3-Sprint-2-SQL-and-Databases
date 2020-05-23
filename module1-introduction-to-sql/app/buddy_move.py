import pandas as pd
import os
import sqlite3
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

my_df = pd.read_csv("./buddymove_holidayiq.csv")
# print(my_df.shape)

my_df.to_sql('review', con=engine, if_exists='replace', index_label='id')

# engine.execute("SELECT * FROM buddymove_holidayiq").fetchall()

DB_FILEPATH = os.path.join(os.path.dirname(
    __file__), "..", "buddymove_holidayiq.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
connection.row_factory = sqlite3.Row
# print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)


query1 = f"INSERT INTO review "
result1 = cursor.execute(query1).fetchone()
print("Number of rows: ", result1)
