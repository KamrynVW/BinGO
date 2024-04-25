import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect("bingoDB.db")

    def createDatabase(self):
        cur = self.conn.cursor()

        # Cards 
        cur.execute("""CREATE TABLE IF NOT EXISTS Cards (
                    CARDID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    COLOUR  VARCHAR(15) NOT NULL,
                    ROW1    VARCHAR(15) NOT NULL,
                    ROW2    VARCHAR(15) NOT NULL,
                    ROW3    VARCHAR(15) NOT NULL,
                    ROW4    VARCHAR(15) NOT NULL,
                    ROW5    VARCHAR(15) NOT NULL);""")
        
        # WinConditions
        cur.execute("""CREATE TABLE IF NOT EXISTS WinConditions (
                    WINID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    NAME    VARCHAR(30),
                    ROW1    VARCHAR(15) NOT NULL,
                    ROW2    VARCHAR(15) NOT NULL,
                    ROW3    VARCHAR(15) NOT NULL,
                    ROW4    VARCHAR(15) NOT NULL,
                    ROW5    VARCHAR(15) NOT NULL);""")
        
        self.conn.commit()

    def addCard(self, colour, row1, row2, row3, row4, row5):
        cur = self.conn.cursor()

        cur.execute("INSERT INTO Cards (COLOUR, ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?,?)",
                    (colour, row1, row2, row3, row4, row5))
        
        self.conn.commit()
        
    def addWinCondition(self, name, row1, row2, row3, row4, row5):
        cur = self.conn.cursor()

        if name is None:
            cur.execute("INSERT INTO WinConditions (ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?)",
                        (row1, row2, row3, row4, row5))
        else:
            cur.execute("INSERT INTO WinConditions (NAME, ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?,?)",
                        (name, row1, row2, row3, row4, row5))
            
        self.conn.commit()