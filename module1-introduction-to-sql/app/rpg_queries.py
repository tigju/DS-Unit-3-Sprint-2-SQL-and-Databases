import os
import sqlite3


DB_FILEPATH = os.path.join(os.path.dirname(
    __file__), "..", "rgp_db.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
connection.row_factory = sqlite3.Row
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)

# how many characters
query1 = "SELECT COUNT(DISTINCT character_id) AS number_of_characters FROM charactercreator_character"
result1 = cursor.execute(query1).fetchall()
print("Number of characters: ", result1)

# how many characters of each subclass
query2 = "SELECT COUNT(DISTINCT Character_ptr_id) AS cleric_number FROM charactercreator_cleric"
result2 = cursor.execute(query2).fetchall()
print("Number of cleric characters: ", result2)

query3 = "SELECT COUNT(DISTINCT Character_ptr_id) AS fighter_number FROM charactercreator_fighter"
result3 = cursor.execute(query3).fetchall()
print("Number of fighter characters: ", result3)

query4 = "SELECT COUNT(DISTINCT Character_ptr_id) AS mage_number FROM charactercreator_mage"
result4 = cursor.execute(query4).fetchall()
print("Number of mage characters: ", result4)

query5 = "SELECT COUNT(DISTINCT mage_ptr_id) AS necromancer_number FROM charactercreator_necromancer"
result5 = cursor.execute(query5).fetchall()
print("Number of necrmancer characters: ", result5)

query6 = "SELECT COUNT(DISTINCT Character_ptr_id) AS thief_number FROM charactercreator_thief"
result6 = cursor.execute(query6).fetchall()
print("Number of thief characters: ", result6)

# how many items
query7 = "SELECT COUNT(DISTINCT item_id) AS number_of_items FROM armory_item"
result7 = cursor.execute(query7).fetchall()
print("Number of items: ", result7)

