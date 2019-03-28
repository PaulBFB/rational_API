import uuid
import sqlite3


#print(uuid.uuid4())
root = uuid.UUID('372e84be-d0e4-4338-b210-fe6ca4ca262b')

test = uuid.uuid5(root, 'test')
print(test)

conn = sqlite3.connect('database.sqlite')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE TEST
(id text,
name text)
""")

conn.commit()
conn.close()
