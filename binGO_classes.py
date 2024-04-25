import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect("bingoDB.db")
        self.createDatabase()

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

    def addCard(self, card):
        cur = self.conn.cursor()

        cur.execute("INSERT INTO Cards (COLOUR, ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?,?)",
                    (card.colour, card.rows[0], card.rows[1], card.rows[2], card.rows[3], card.rows[4]))
        
        self.conn.commit()
        
    def addWinCondition(self, winCondition):
        cur = self.conn.cursor()

        if winCondition.name is None:
            cur.execute("INSERT INTO WinConditions (ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?)",
                        (winCondition.rows[0], winCondition.rows[1], winCondition.rows[2], winCondition.rows[3], winCondition.rows[4]))
        else:
            cur.execute("INSERT INTO WinConditions (NAME, ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?,?)",
                        (winCondition.name, winCondition.rows[0], winCondition.rows[1], winCondition.rows[2], winCondition.rows[3], winCondition.rows[4]))
            
        self.conn.commit()

class Card():
    def __init__(self, name, row1, row2, row3, row4, row5):
        self.name = name
        self.rows = [row1, row2, row3, row4, row5]

    def setName(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def setRow(self, rowNum, newRow):
        self.rows[rowNum] = newRow

    def getRow(self, rowNum):
        return self.rows[rowNum]
    
if __name__ == '__main__':
    db = Database()
    newBingoCard = Card("red", "1,16,31,46,61", "2,17,32,47,62", "3,18,33,48,63", "4,19,34,49,64", "5,20,35,50,65")
    newWin = Card("full", "1,1,1,1,1", "1,1,1,1,1", "1,1,1,1,1", "1,1,1,1,1", "1,1,1,1,1")
    db.addCard(newBingoCard)