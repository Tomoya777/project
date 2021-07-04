import sqlite3

# Create database in memory
conn = sqlite3.connect('test.db')

curs = conn.cursor()


# Save (commit) the changes
conn.commit()

# Browse inserted data
for row in curs.execute('SELECT * FROM taskdata'):
    print(row)

curs.close()
conn.close()