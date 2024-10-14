import sqlite3


class Person:
    def __init__(self, name, url, type, id=None):
        self.id = id
        self.name = name
        self.url = url
        self.type = type

    def save(self):
        conn = sqlite3.connect('db/db.sqlite')
        c = conn.cursor()
        if self.id is None:
            c.execute("INSERT INTO people (name, url, type) VALUES (?, ?, ?)",
                      (self.name, self.url, self.type))
            self.id = c.lastrowid  # Retrieve the last inserted row ID
        else:
            c.execute("INSERT INTO people (id, name, url, type) VALUES (?, ?, ?, ?)",
                      (self.id, self.name, self.url, self.type))
        conn.commit()
        conn.close()

    @staticmethod
    def search(name):
        conn = sqlite3.connect('db/db.sqlite')
        c = conn.cursor()
        c.execute("SELECT * FROM people WHERE name=?", (name,))
        result = c.fetchone()  # Fetch only one row
        conn.close()
        if result:
            return Person(*result)  # Create a Person object from the result
        else:
            return None  # Return None if no matching person found
