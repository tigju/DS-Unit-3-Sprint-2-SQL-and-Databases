import pandas as pd
import os
import sqlite3
from sqlalchemy import create_engine

my_df = pd.read_csv("./buddymove_holidayiq.csv")
# print(my_df.shape)
engine = create_engine('sqlite:///buddymove_holidayiq.db')
my_df.to_sql('review', con=engine, if_exists='replace', index_label='id')

# engine.execute("SELECT * FROM buddymove_holidayiq").fetchall()

DB_FILEPATH = os.path.join(os.path.dirname(
    __file__), "..", "buddymove_holidayiq.db")

connection = sqlite3.connect(DB_FILEPATH)
connection.row_factory = sqlite3.Row
# print("CONNECTION:", connection)

cursor = connection.cursor()
# print("CURSOR", cursor)


query1 = """
        SELECT
        COUNT(DISTINCT `User Id`) AS users
        FROM review
        WHERE Nature >= 100 AND Shopping >= 100
        """
result1 = cursor.execute(query1).fetchone()
print("Number of users who reviewed at least 100 in Nature and at least 100 in the Shopping category: ",
      result1[0])

query2 = """
        SELECT 
	        SUM(review.Sports)/COUNT(review.Sports) AS avg_sports,
	        SUM(review.Religious)/COUNT(review.Religious) AS avg_religious,
	        SUM(review.Nature)/COUNT(review.Nature) AS avg_nature,
 	        SUM(review.Theatre)/COUNT(review.Theatre) AS avg_theatre,
	        SUM(review.Shopping)/COUNT(review.Shopping) AS avg_shopping,
	        SUM(review.Picnic)/COUNT(review.Picnic) AS avg_picnic
        FROM review;
        """
result2 = cursor.execute(query2).fetchone()
print("average number of reviews for each category:")

print(f'Sports: {result2["avg_sports"]}, Religious: {result2["avg_religious"]}, Nature: {result2["avg_nature"]}, Theatre: {result2["avg_theatre"]}, Shopping: {result2["avg_shopping"]}, Picnic: {result2["avg_picnic"]}')
