import sqlite3

# SQLite database usage
class Database():
    # Initialize database bingoDB and create tables
    def __init__(self):
        self.conn = sqlite3.connect("bingoDB.db")
        self.createDatabase()

    # Create base tables of database
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
        cur.close()

    # Add a new card to the database
    def addCard(self, card):
        cur = self.conn.cursor()

        cur.execute("INSERT INTO Cards (COLOUR, ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?,?)",
                    (card.name, card.rows[0], card.rows[1], card.rows[2], card.rows[3], card.rows[4]))
        
        self.conn.commit()
        cur.close()

    # Recover and create a new Card object from the database at a given id
    def writeCard(self, id):
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM Cards WHERE CARDID = ?", (id,))
        data = cur.fetchone()
    
        card = Card(data[1], data[2], data[3], data[4], data[5], data[6])

        cur.close()

        return card
        
    # Add a win condition to the database
    def addWinCondition(self, winCondition):
        cur = self.conn.cursor()

        if winCondition.name is None:
            cur.execute("INSERT INTO WinConditions (ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?)",
                        (winCondition.rows[0], winCondition.rows[1], winCondition.rows[2], winCondition.rows[3], winCondition.rows[4]))
        else:
            cur.execute("INSERT INTO WinConditions (NAME, ROW1, ROW2, ROW3, ROW4, ROW5) VALUES (?,?,?,?,?,?)",
                        (winCondition.name, winCondition.rows[0], winCondition.rows[1], winCondition.rows[2], winCondition.rows[3], winCondition.rows[4]))
            
        self.conn.commit()
        cur.close()

    # Recover and create a new Card object representing a win condition from the database at a given id
    def writeWinCondition(self, id):
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM WinConditions WHERE WINID = ?", (id,))
        data = cur.fetchone()

        win = Card(data[1], data[2], data[3], data[4], data[5], data[6])

        cur.close()

        return win

    # Get all IDs based on a specified colour    
    def getCardsByColour(self, colour):
        cur = self.conn.cursor()

        cur.execute("SELECT CARDID FROM Cards WHERE COLOUR = ?", (colour,))
        data = cur.fetchall()
        
        cardIDs = []

        for values in data:
            cardIDs.append(values[0])

        return cardIDs
    
class Card():
    # Initialize a new card object with a name (either colour or WC name), and 5 rows of values
    def __init__(self, name, row1, row2, row3, row4, row5):
        self.name = name
        self.rows = [row1, row2, row3, row4, row5]

    # Set name of WC/Card
    def setName(self, name):
        self.name = name
    
    # Get name of WC/Card
    def getName(self):
        return self.name
    
    # Set a specific row to new values
    def setRow(self, rowNum, newRow):
        self.rows[rowNum] = newRow

    # Get the values in a specified row
    def getRow(self, rowNum):
        return self.rows[rowNum]
    
if __name__ == '__main__':
    db = Database()
    newBingoCard = Card("red", "1,16,31,46,61", "2,17,32,47,62", "3,18,33,48,63", "4,19,34,49,64", "5,20,35,50,65")
    newBingoCard1 = Card("orange", "1,16,31,46,61", "2,17,32,47,62", "3,18,33,48,63", "4,19,34,49,64", "5,20,35,50,65")
    newBingoCard2 = Card("red", "1,16,31,46,61", "2,17,32,47,62", "3,18,33,48,63", "4,19,34,49,64", "5,20,35,50,65")
    newBingoCard3 = Card("orange", "1,16,31,46,61", "2,17,32,47,62", "3,18,33,48,63", "4,19,34,49,64", "5,20,35,50,65")
    newBingoCard4 = Card("red", "1,16,31,46,61", "2,17,32,47,62", "3,18,33,48,63", "4,19,34,49,64", "5,20,35,50,65")
    newWin = Card("full", "1,1,1,1,1", "1,1,1,1,1", "1,1,1,1,1", "1,1,1,1,1", "1,1,1,1,1")
    db.addCard(newBingoCard)
    db.addCard(newBingoCard1)
    db.addCard(newBingoCard2)
    db.addCard(newBingoCard3)
    db.addCard(newBingoCard4)
    card = db.writeCard(1)
    values = db.getCardsByColour("red")