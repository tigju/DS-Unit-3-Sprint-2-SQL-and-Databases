import os
import sqlite3


DB_FILEPATH = os.path.join(os.path.dirname(
    __file__), "..", "rpg_db.sqlite3")

connection = sqlite3.connect(DB_FILEPATH)
connection.row_factory = sqlite3.Row
# print("CONNECTION:", connection)

cursor = connection.cursor()
# print("CURSOR", cursor)

# how many characters
query1 = """
        SELECT COUNT(DISTINCT character_id) 
        AS number_of_characters 
        FROM charactercreator_character
        """
result1 = cursor.execute(query1).fetchone()
print("Number of characters: ", result1[0])

# how many characters of each subclass
query2 = """
        SELECT COUNT(DISTINCT character_ptr_id)
        AS cleric_number FROM charactercreator_cleric
        """
result2 = cursor.execute(query2).fetchone()
print("Number of cleric characters: ", result2[0])

query3 = """
        SELECT COUNT(DISTINCT character_ptr_id) 
        AS fighter_number FROM charactercreator_fighter
        """
result3 = cursor.execute(query3).fetchone()
print("Number of fighter characters: ", result3[0])

query4 = """
        SELECT COUNT(DISTINCT character_ptr_id) 
        AS mage_number FROM charactercreator_mage
        """
result4 = cursor.execute(query4).fetchone()
print("Number of mage characters: ", result4[0])

query5 = """
        SELECT COUNT(DISTINCT mage_ptr_id) 
        AS necromancer_number FROM charactercreator_necromancer
        """
result5 = cursor.execute(query5).fetchone()
print("Number of necrmancer characters: ", result5[0])

query6 = """
        SELECT COUNT(DISTINCT character_ptr_id) 
        AS thief_number FROM charactercreator_thief
        """
result6 = cursor.execute(query6).fetchone()
print("Number of thief characters: ", result6[0])

# how many items
query7 = """
        SELECT COUNT(DISTINCT item_id) 
        AS number_of_items FROM armory_item
        """
result7 = cursor.execute(query7).fetchone()
print("Number of items: ", result7[0])

# how many weapon items
query8 = """
        SELECT COUNT(DISTINCT item_ptr_id) 
        AS weapon_number FROM armory_weapon
        """
result8 = cursor.execute(query8).fetchone()
print("Number of weapon items: ", result8[0])

# how many items are not weapons

query9 = """
        SELECT COUNT(DISTINCT item_id) 
        FROM armory_item WHERE item_id 
            NOT IN 
            (SELECT item_ptr_id FROM armory_weapon)
        """
result9 = cursor.execute(query9).fetchone()
print("Number of non-weapon items: ", result9[0])

# how many items each character have
query10 = """
        SELECT charactercreator_character.name AS character_name,
	    COUNT(DISTINCT charactercreator_character_inventory.item_id) AS item_number
        FROM charactercreator_character_inventory
        LEFT JOIN charactercreator_character  ON charactercreator_character.character_id = charactercreator_character_inventory.character_id
        LEFT JOIN armory_item  ON charactercreator_character_inventory.item_id = armory_item.item_id
        GROUP BY charactercreator_character_inventory.character_id
        LIMIT 20;
        """
result10 = cursor.execute(query10).fetchall()
print("Number of items each character have: ", dict(result10))

query11 = """
        SELECT charactercreator_character.name AS character_name,
        count(distinct armory_weapon.item_ptr_id) as weapon_count
        FROM charactercreator_character
        LEFT JOIN charactercreator_character_inventory 
        ON charactercreator_character.character_id = charactercreator_character_inventory.character_id
        LEFT JOIN armory_weapon ON armory_weapon.item_ptr_id = charactercreator_character_inventory.item_id
        GROUP BY charactercreator_character.character_id
        LIMIT 20;
        """
result11 = cursor.execute(query11).fetchall()
print("Number of weapons each character have: ", dict(result11))

# how many items each character have on average
query12 = """
        SELECT charactercreator_character.name AS character_name,
	    AVG(DISTINCT charactercreator_character_inventory.item_id) AS item_average
        FROM charactercreator_character_inventory
        LEFT JOIN charactercreator_character  ON charactercreator_character.character_id = charactercreator_character_inventory.character_id
        LEFT JOIN armory_item  ON charactercreator_character_inventory.item_id = armory_item.item_id
        GROUP BY charactercreator_character.character_id
        """
result12 = cursor.execute(query12).fetchall()
print("Number of items each character have: ", dict(result12))
