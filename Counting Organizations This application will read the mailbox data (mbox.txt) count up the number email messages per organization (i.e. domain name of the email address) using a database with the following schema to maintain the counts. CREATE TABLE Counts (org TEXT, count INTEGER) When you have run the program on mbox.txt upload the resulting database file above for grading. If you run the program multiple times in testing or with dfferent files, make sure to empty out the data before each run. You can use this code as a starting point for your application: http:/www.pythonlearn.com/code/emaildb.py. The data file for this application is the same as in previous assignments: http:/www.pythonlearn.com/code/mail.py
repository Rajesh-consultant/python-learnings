import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fh = open('F:/Users/rajes/OneDrive/Desktop/Atom/sql/mbox.txt', 'r')
list_1 = []
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split('@')
    org= pieces[1]
    org = org.rstrip()

    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    try:
        count = cur.fetchone()[0]
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',(org,))
    except:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))

        
conn.commit()
# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])
cur.close()
