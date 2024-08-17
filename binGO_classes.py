import sqlite3
import os

DB_FILE_PATH = os.path.join(os.path.dirname(__file__), 'bingoDB.db')

# Class: Database
#
# Uses SQLite to initialize and utilize a database
# that stores both cards and win conditions. Also
# has the capability to create a card and win
# condition object and return it.

class Database():

    # Method: Initialize
    # 
    # Initializes or connects to a database and creates the needed tables.
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE_PATH)
        self.createDatabase()

    # Method: Create Database
    #
    # Creates a cursor and creates any tables that do not already exist.
    def createDatabase(self):
        cur = self.conn.cursor()

        # Cards 
        cur.execute("""CREATE TABLE IF NOT EXISTS Cards (
                    CARDID      INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    COLOUR      VARCHAR(15) NOT NULL,
                    MIDDLEID    INTEGER NOT NULL,
                    BACKID      INTEGER NOT NULL,
                    COLUMNB     VARCHAR(15) NOT NULL,
                    COLUMNI     VARCHAR(15) NOT NULL,
                    COLUMNN     VARCHAR(15) NOT NULL,
                    COLUMNG     VARCHAR(15) NOT NULL,
                    COLUMNO     VARCHAR(15) NOT NULL);""")
        
        # WinConditions
        cur.execute("""CREATE TABLE IF NOT EXISTS WinConditions (
                    WINID       INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    NAME        VARCHAR(30),
                    COLUMNB     VARCHAR(15) NOT NULL,
                    COLUMNI     VARCHAR(15) NOT NULL,
                    COLUMNN     VARCHAR(15) NOT NULL,
                    COLUMNG     VARCHAR(15) NOT NULL,
                    COLUMNO     VARCHAR(15) NOT NULL);""")
        
        self.conn.commit()
        cur.close()

    # Method: Read Card
    #
    # Read a card object and create an entry in the database for it.
    def readCard(self, card):
        cur = self.conn.cursor()

        # Format the columns into string that database uses
        b_col_string = ','.join(str(sublist[0]) for sublist in card.bCol)
        i_col_string = ','.join(str(sublist[0]) for sublist in card.iCol)
        n_col_string = ','.join(str(sublist[0]) for sublist in card.nCol)
        g_col_string = ','.join(str(sublist[0]) for sublist in card.gCol)
        o_col_string = ','.join(str(sublist[0]) for sublist in card.oCol)

        # Insert card into database
        cur.execute("INSERT INTO Cards (COLOUR, MIDDLEID, BACKID, COLUMNB, COLUMNI, COLUMNN, COLUMNG, COLUMNO) VALUES (?,?,?,?,?,?,?,?)", 
                   (card.colour, card.middleId, card.backId, b_col_string, i_col_string, n_col_string, g_col_string, o_col_string))
        
        self.conn.commit()
        cur.close()

    # Method: Write Card
    #
    # Create a card object from the provided ID and returns it.
    def writeCard(self, id):
        cur = self.conn.cursor()

        # Get the card at the provided ID
        cur.execute("SELECT * FROM Cards WHERE CARDID = ?", (id,))
        data = cur.fetchone()

        # Split the 5 columns on commas to create a list of numbers used in card creation.
        b_col_list = []
        b_col_values = data[4].split(',')

        for value in b_col_values:
            b_col_list.append(int(value))

        i_col_list = []
        i_col_values = data[5].split(',')

        for value in i_col_values:
            i_col_list.append(int(value))

        n_col_list = []
        n_col_values = data[6].split(',')

        for value in n_col_values:
            n_col_list.append(int(value))

        g_col_list = []
        g_col_values = data[7].split(',')

        for value in g_col_values:
            g_col_list.append(int(value))

        o_col_list = []
        o_col_values = data[8].split(',')

        for value in o_col_values:
            o_col_list.append(int(value))

        # Create the new card object and return it
        card = Card(data[1], data[2], data[3], b_col_list, i_col_list, n_col_list, g_col_list, o_col_list)
        cur.close()
        return card

    # Method: Get Cards By Colour
    # 
    # Returns a list containing all IDs of cards that match the provided colour. 
    def getCardsByColour(self, colour):
        cur = self.conn.cursor()

        # Get all Card IDs from the database with a specific colour attribute
        cur.execute("SELECT CARDID FROM Cards WHERE COLOUR = ?", (colour,))
        data = cur.fetchall()

        # If there are no cards at that colour, close cursor and return
        if len(data) == 0:
            cur.close()
            return None
        
        # Create and return list of all fitting card IDs
        cardIDs = []
        for values in data:
            cardIDs.append(values[0])

        cur.close()
        return cardIDs
    
    # Method: Get ID Of Colour
    #
    # Get the ID of a specific card within a certain colour.
    def getIdOfColour(self, cardNum, cardCol):
        cur = self.conn.cursor()

        # Select all Card IDs from the database at a specific colour and save them in a list
        cur.execute("SELECT CARDID FROM Cards WHERE COLOUR = ?", (cardCol,))
        data = cur.fetchall()
        indexes = [row[0] for row in data]

        cur.close()
        return indexes[cardNum - 1]
    
    # Method: Read Win
    #
    # Read a win condition object and create an entry in the database for it.
    def readWin(self, win):
        cur = self.conn.cursor()

        # Format the win condition into the format it is stored in
        b_col_string = ','.join(str(value) for value in win.col[0])
        i_col_string = ','.join(str(value) for value in win.col[1])
        n_col_string = ','.join(str(value) for value in win.col[2])
        g_col_string = ','.join(str(value) for value in win.col[3])
        o_col_string = ','.join(str(value) for value in win.col[4])

        # If the win condition goes unnamed, name it based on the ID number
        noName = False
        if win.name is None:
            noName = True

        # Insert the win condition into the database
        cur.execute("INSERT INTO WinConditions (NAME, COLUMNB, COLUMNI, COLUMNN, COLUMNG, COLUMNO) VALUES (?,?,?,?,?,?)", 
                    (win.name, b_col_string, i_col_string, n_col_string, g_col_string, o_col_string))
        ID = cur.lastrowid
        
        if noName:
            cur.execute("UPDATE WinConditions SET NAME = ? WHERE WINID = ?", (f"Win-{ID}", ID))
        
        cur.close()
        self.conn.commit()

    # Method: Write Win
    # 
    # Write a win condition object from the provided ID and returns it.
    def writeWin(self, id):
        cur = self.conn.cursor()

        # Get all data from a win condition at a specific ID
        cur.execute("SELECT * FROM WinConditions WHERE WINID = ?", (id,))
        data = cur.fetchone()

        # Compile the BINGO columns from the stored database strings
        b_col_list = []
        b_col_values = data[2].split(',')

        for value in b_col_values:
            b_col_list.append(int(value))

        i_col_list = []
        i_col_values = data[3].split(',')

        for value in i_col_values:
            i_col_list.append(int(value))

        n_col_list = []
        n_col_values = data[4].split(',')

        for value in n_col_values:
            n_col_list.append(int(value))

        g_col_list = []
        g_col_values = data[5].split(',')

        for value in g_col_values:
            g_col_list.append(int(value))

        o_col_list = []
        o_col_values = data[6].split(',')

        for value in o_col_values:
            o_col_list.append(int(value))

        # Create and return the win condition
        win = WinCondition(data[1], b_col_list, i_col_list, n_col_list, g_col_list, o_col_list)
        cur.close()
        return win
    
    # Method: Get Win ID By Name
    #
    # Get the ID of a win condition based on the provided name.
    def getWinIdByName(self, name):
        cur = self.conn.cursor()

        # Search the name and get the ID if it exists, return None otherwise
        cur.execute("SELECT WINID FROM WinConditions WHERE NAME = ?", (name,))
        data = cur.fetchone()
        cur.close()

        if data is not None:
            return data[0]
        else:
            return None
    
    # Method: Get All Win Names
    #
    # Get all names of entered wins and return a compiled list of them.
    def getAllWinNames(self):
        cur = self.conn.cursor()

        # Get and compile all names of win conditions
        cur.execute("SELECT NAME FROM WinConditions")
        data = cur.fetchall()

        names = [name[0] for name in data]

        cur.close()
        return names

    # Method: Delete Card
    #
    # Deletes a card from the database at a provided ID.
    def deleteCard(self, id):
        cur = self.conn.cursor()

        cur.execute("DELETE FROM Cards WHERE CARDID = ?", (id,))

        self.conn.commit()
        cur.close()

    # Method: Change Card
    #
    # Modify the card at a provided ID with the updated values provided.
    def changeCard(self, id, middleID, backID, bCol, iCol, nCol, gCol, oCol, colour):
        cur = self.conn.cursor()

        cur.execute("UPDATE Cards SET COLOUR = ?, MIDDLEID = ?, BACKID = ?, COLUMNB = ?, COLUMNI = ?, COLUMNN = ?, COLUMNG = ?, COLUMNO = ? WHERE CARDID = ?",
                    (colour, middleID, backID, bCol, iCol, nCol, gCol, oCol, id))
        
        self.conn.commit()
        cur.close()

    # Method: Delete Win
    #
    # Delete a win condition from the database at a provided ID.
    def deleteWin(self, id):
        cur = self.conn.cursor()

        cur.execute("DELETE FROM WinConditions WHERE WINID = ?", (id,))

        self.conn.commit()
        cur.close()

    # Method: Change Win
    #
    # Modify the win condition at a provied ID with the updated values provided.
    def changeWin(self, id, name, bCol, iCol, nCol, gCol, oCol):
        cur = self.conn.cursor()

        cur.execute("UPDATE WinConditions SET NAME = ?, COLUMNB = ?, COLUMNI = ?, COLUMNN = ?, COLUMNG = ?, COLUMNO = ? WHERE WINID = ?",
                    (name, bCol, iCol, nCol, gCol, oCol, id))
        
        self.conn.commit()
        cur.close()

# Class: Card
#
# A card class that utilizes a 2D array
# as well as a colour string and 2 identification
# IDs that allows for flexible playing according
# to a provided win condition.

class Card():

    # Method: Initialize
    #
    # Initialize a card object with a colour, back and middle ID, and 5 columns.

    def __init__(self, colour, id1, id2, col1, col2, col3, col4, col5):
        self.colour = colour
        self.middleId = id1
        self.backId = id2
        self.bCol = [[col1[0], 0], [col1[1], 0], [col1[2], 0], [col1[3], 0], [col1[4], 0]]
        self.iCol = [[col2[0], 0], [col2[1], 0], [col2[2], 0], [col2[3], 0], [col2[4], 0]]
        self.nCol = [[col3[0], 0], [col3[1], 0], [col3[2], 0], [col3[3], 0], [col3[4], 0]]
        self.gCol = [[col4[0], 0], [col4[1], 0], [col4[2], 0], [col4[3], 0], [col4[4], 0]]
        self.oCol = [[col5[0], 0], [col5[1], 0], [col5[2], 0], [col5[3], 0], [col5[4], 0]]

    # Method: String
    #
    # Return a string representation of a card.
    def __str__(self):
        result = f"\n{self.colour}:\n{self.bCol[0][0]} {self.iCol[0][0]} {self.nCol[0][0]} {self.gCol[0][0]} {self.oCol[0][0]}\n"
        result += f"{self.bCol[1][0]} {self.iCol[1][0]} {self.nCol[1][0]} {self.gCol[1][0]} {self.oCol[1][0]}\n"
        result += f"{self.bCol[2][0]} {self.iCol[2][0]} {self.nCol[2][0]} {self.gCol[2][0]} {self.oCol[2][0]}\n"
        result += f"{self.bCol[3][0]} {self.iCol[3][0]} {self.nCol[3][0]} {self.gCol[3][0]} {self.oCol[3][0]}\n"
        result += f"{self.bCol[4][0]} {self.iCol[4][0]} {self.nCol[4][0]} {self.gCol[4][0]} {self.oCol[4][0]}\n"

        return result

    # Method: Flip Tile Bit
    #
    # Check if the value is in the card AND in the win condition, and flip the called bit if true.
    # In order to speed up search, it checks the BINGO column the value would be in before searching.
    def flipTileBit(self, value, winCondition):
        i = 0
        didFlipBit = 0
        
        if value == 0 and winCondition.col[2][2] == 1:
            self.nCol[2][1] = 1

        # B
        elif value >= 1 and value <= 15:
            for tileValue in self.bCol:
                if tileValue[0] == value and winCondition.col[0][i] == 1:
                    tileValue[1] = 1
                    didFlipBit = 1
                
                i += 1

        # I
        elif value >= 16 and value <= 30:
            for tileValue in self.iCol:
                if tileValue[0] == value and winCondition.col[1][i] == 1:
                    tileValue[1] = 1
                    didFlipBit = 1

                i += 1

        # N
        elif value >= 31 and value <= 45:
            for tileValue in self.nCol:
                if tileValue[0] == value and winCondition.col[2][i] == 1:
                    tileValue[1] = 1
                    didFlipBit = 1

                i += 1

        # G
        elif value >= 46 and value <= 60:
            for tileValue in self.gCol:
                if tileValue[0] == value and winCondition.col[3][i] == 1:
                    tileValue[1] = 1
                    didFlipBit = 1

                i += 1

        # O
        elif value >= 61 and value <= 75:
            for tileValue in self.oCol:
                if tileValue[0] == value and winCondition.col[4][i] == 1:
                    tileValue[1] = 1
                    didFlipBit = 1

                i += 1

        # Return 0 if the number DNE, or a boolean as to whether the card is a winner or not.
        if didFlipBit:
            return winCondition.checkWin(self)
        else:
            return 0
        
    # Method: Revoke Call
    #
    # Check if the value is in a card, win condition, and is called, and flips the bit if true.
    def revokeCall(self, value, winCondition):
        i = 0

        # B
        if value >= 1 and value <= 15:
            for tileValue in self.bCol:
                if tileValue[0] == value and winCondition.col[0][i] == 1:
                    tileValue[1] = 0

                i += 1

        # I
        elif value >= 16 and value <= 30:
            for tileValue in self.iCol:
                if tileValue[0] == value and winCondition.col[1][i] == 1:
                    tileValue[1] = 0

                i += 1

        # N
        elif value >= 31 and value <= 45:
            for tileValue in self.nCol:
                if tileValue[0] == value and winCondition.col[2][i] == 1:
                    tileValue[1] = 0

                i += 1

        # G
        elif value >= 46 and value <= 60:
            for tileValue in self.gCol:
                if tileValue[0] == value and winCondition.col[3][i] == 1:
                    tileValue[1] = 0

                i += 1

        # O
        elif value >= 61 and value <= 75:
            for tileValue in self.oCol:
                if tileValue[0] == value and winCondition.col[4][i] == 1:
                    tileValue[1] = 0

                i += 1
        
    # Method: Reapply Win
    #
    # Unflip all of the called bits, and apply all called numbers according to a new provided win condition.
    def reapplyWin(self, winCondition, numbers):
        for tile in self.bCol:
            tile[1] = 0

        for tile in self.iCol:
            tile[1] = 0

        for tile in self.nCol:
            tile[1] = 0

        for tile in self.gCol:
            tile[1] = 0

        for tile in self.oCol:
            tile[1] = 0

        # Run all of the checks on the numbers, and if any successfully flipped, return 1. Otherwise, return 0.
        win = []
        for number in numbers:
            win.append(self.flipTileBit(number, winCondition))

        if 1 in win:
            return 1
        else:
            return 0

    # Method: Check win proximity
    #
    # Return an array of all missing numbers on a card based on the current win condition.
    def checkWinProx(self, winCondition):
        i = 0
        missingNum = []

        for tile in self.bCol:
            if tile[1] == 0 and winCondition.col[0][i] == 1:
                missingNum.append(tile[0])

            i += 1

        i = 0

        for tile in self.iCol:
            if tile[1] == 0 and winCondition.col[1][i] == 1:
                missingNum.append(tile[0])

            i += 1

        i = 0

        for tile in self.nCol:
            if tile[1] == 0 and winCondition.col[2][i] == 1:
                missingNum.append(tile[0])

            i += 1

        i = 0

        for tile in self.gCol:
            if tile[1] == 0 and winCondition.col[3][i] == 1:
                missingNum.append(tile[0])

            i += 1

        i = 0

        for tile in self.oCol:
            if tile[1] == 0 and winCondition.col[4][i] == 1:
                missingNum.append(tile[0])

            i += 1

        return missingNum

# Class: Win Condition
#
# A win condition class that utilizes
# a name as well as 5 columns (matching the
# Card class) to allow for customized win
# conditions that can be checked against.

class WinCondition():

    # Method: Initialize
    #
    # Initialize a win condition with a name and 5 columns of binary bits,
    # representing if the tile is needed or not.
    def __init__(self, name, col1, col2, col3, col4, col5):
        self.name = name
        self.col = [col1, col2, col3, col4, col5]

    # Method: String
    #
    # Return a string representation of a win condition.
    def __str__(self):
        result = f"{self.name}:\n{self.col[0][0]} {self.col[1][0]} {self.col[2][0]} {self.col[3][0]} {self.col[4][0]}\n"
        result += f"{self.col[0][1]} {self.col[1][1]} {self.col[2][1]} {self.col[3][1]} {self.col[4][1]}\n"
        result += f"{self.col[0][2]} {self.col[1][2]} {self.col[2][2]} {self.col[3][2]} {self.col[4][2]}\n"
        result += f"{self.col[0][3]} {self.col[1][3]} {self.col[2][3]} {self.col[3][3]} {self.col[4][3]}\n"
        result += f"{self.col[0][4]} {self.col[1][4]} {self.col[2][4]} {self.col[3][4]} {self.col[4][4]}\n"

        return result
    
    # Method: Get Total Required Tiles
    #
    # Get the total amount of tiles needed to complete the win condition.
    def getTotalRequiredTiles(self):
        total = 0

        for col in self.col:
            for bit in col:
                total += bit

        return total
    
    # Method: Check Win
    #
    # Check if a card has won by taking each column and comparing the binary called bit against the
    # appropriate column of the win condition.
    def checkWin(self, card):
        bColBits = []
        for value in card.bCol:
            bColBits.append(value[1])
        iColBits = []
        for value in card.iCol:
            iColBits.append(value[1])
        nColBits = []
        for value in card.nCol:
            nColBits.append(value[1])
        gColBits = []
        for value in card.gCol:
            gColBits.append(value[1])
        oColBits = []
        for value in card.oCol:
            oColBits.append(value[1])

        if bColBits == self.col[0] and iColBits == self.col[1] and nColBits == self.col[2] and gColBits == self.col[3] and oColBits == self.col[4]:
            return 1
        else:
            return 0
        