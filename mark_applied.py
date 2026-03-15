import sqlite3

url = input("Paste job URL: ").strip()

conn = sqlite3.connect("jobs.db")
cursor = conn.cursor()

cursor.execute("UPDATE jobs SET applied = 1 WHERE url = ?", (url,))
affected = cursor.rowcount

conn.commit()
conn.close()

if affected:
    print(f"Marked as applied: {url}")
    print("Run main.py to refresh the Excel file with the updated status.")
else:
    print("No job found with that URL.")