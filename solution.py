import json
import sqlite3

# Create and connect to the database
conn = sqlite3.connect('roster_data.sqlite')
cur = conn.cursor()

# Drop existing tables if they exist
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Member;
''')

# Create the tables
cur.executescript('''
CREATE TABLE User (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE
);

CREATE TABLE Member (
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

# Read the JSON data from the file
filename = 'roster_data.json'
data = open(filename).read()
json_data = json.loads(data)

# Insert data into User, Course, and Member tables
for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    cur.execute('''INSERT OR IGNORE INTO User (name) VALUES ( ? )''', (name, ))
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title) VALUES ( ? )''', (title, ))
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role) 
        VALUES ( ?, ?, ? )''', (user_id, course_id, role))

    conn.commit()

# Execute the first SQL command
sql_command1 = '''
SELECT User.name, Course.title, Member.role FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2
'''

for row in cur.execute(sql_command1):
    print('|'.join([str(item) for item in row]))

# Execute the second SQL command
sql_command2 = '''
SELECT 'XYZZY' || hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X LIMIT 1
'''

for row in cur.execute(sql_command2):
    print(row[0])

cur.close()
