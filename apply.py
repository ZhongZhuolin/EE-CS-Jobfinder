import sqlite3

url = input("Paste job URL: ")

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute(
    "UPDATE jobs SET applied = 1 WHERE url = ?",
    (url,)
)

conn.commit()
conn.close()

print("Marked as applied.")