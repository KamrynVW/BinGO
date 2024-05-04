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

    def readCard(self, card):
        cur = self.conn.cursor()
        b_col_string = ','.join(str(sublist[0]) for sublist in card.bCol)
        i_col_string = ','.join(str(sublist[0]) for sublist in card.iCol)
        n_col_string = ','.join(str(sublist[0]) for sublist in card.nCol)
        g_col_string = ','.join(str(sublist[0]) for sublist in card.gCol)
        o_col_string = ','.join(str(sublist[0]) for sublist in card.oCol)

        cur.execute("INSERT INTO Cards (COLOUR, MIDDLEID, BACKID, COLUMNB, COLUMNI, COLUMNN, COLUMNG, COLUMNO) VALUES (?,?,?,?,?,?,?,?)", 
                   (card.colour, card.middleId, card.backId, b_col_string, i_col_string, n_col_string, g_col_string, o_col_string))
        
        self.conn.commit()
        cur.close()

    def writeCard(self, id):
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM Cards WHERE CARDID = ?", (id,))
        data = cur.fetchone()

        # 0 = id, 1 = colour, 2 = middleid, 3 = backid, 4 = b, 5 = i, 6 = n, 7 = g, 8 = o
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

        card = Card(data[1], data[2], data[3], b_col_list, i_col_list, n_col_list, g_col_list, o_col_list)

        cur.close()
        return card

    # Get all IDs based on a specified colour    
    def getCardsByColour(self, colour):
        cur = self.conn.cursor()

        cur.execute("SELECT CARDID FROM Cards WHERE COLOUR = ?", (colour,))
        data = cur.fetchall()
        if len(data) == 0:
            cur.close()
            return None
        
        cardIDs = []

        for values in data:
            cardIDs.append(values[0])

        cur.close()

        return cardIDs
    
    def readWin(self, win):
        cur = self.conn.cursor()

        b_col_string = ','.join(str(value) for value in win.col[0])
        i_col_string = ','.join(str(value) for value in win.col[1])
        n_col_string = ','.join(str(value) for value in win.col[2])
        g_col_string = ','.join(str(value) for value in win.col[3])
        o_col_string = ','.join(str(value) for value in win.col[4])

        cur.execute("INSERT INTO WinConditions (NAME, COLUMNB, COLUMNI, COLUMNN, COLUMNG, COLUMNO) VALUES (?,?,?,?,?,?)", 
                    (win.name, b_col_string, i_col_string, n_col_string, g_col_string, o_col_string))
        
        cur.close()
        self.conn.commit()

    def writeWin(self, id):
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM WinConditions WHERE WINID = ?", (id,))
        data = cur.fetchone()

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

        win = WinCondition(data[1], b_col_list, i_col_list, n_col_list, g_col_list, o_col_list)
        cur.close()
        return win
    
    def getWinIdByName(self, name):
        cur = self.conn.cursor()

        cur.execute("SELECT WINID FROM WinConditions WHERE NAME = ?", (name,))
        data = cur.fetchone()
        cur.close()

        if data is not None:
            return data[0]
        else:
            return None
    
class Card():
    def __init__(self, colour, id1, id2, col1, col2, col3, col4, col5):
        self.colour = colour
        self.middleId = id1
        self.backId = id2
        self.bCol = [[col1[0], 0], [col1[1], 0], [col1[2], 0], [col1[3], 0], [col1[4], 0]]
        self.iCol = [[col2[0], 0], [col2[1], 0], [col2[2], 0], [col2[3], 0], [col2[4], 0]]
        self.nCol = [[col3[0], 0], [col3[1], 0], [col3[2], 0], [col3[3], 0], [col3[4], 0]]
        self.gCol = [[col4[0], 0], [col4[1], 0], [col4[2], 0], [col4[3], 0], [col4[4], 0]]
        self.oCol = [[col5[0], 0], [col5[1], 0], [col5[2], 0], [col5[3], 0], [col5[4], 0]]

    def __str__(self):
        result = f"\n{self.colour}:\n{self.bCol[0][0]} {self.iCol[0][0]} {self.nCol[0][0]} {self.gCol[0][0]} {self.oCol[0][0]}\n"
        result += f"{self.bCol[1][0]} {self.iCol[1][0]} {self.nCol[1][0]} {self.gCol[1][0]} {self.oCol[1][0]}\n"
        result += f"{self.bCol[2][0]} {self.iCol[2][0]} {self.nCol[2][0]} {self.gCol[2][0]} {self.oCol[2][0]}\n"
        result += f"{self.bCol[3][0]} {self.iCol[3][0]} {self.nCol[3][0]} {self.gCol[3][0]} {self.oCol[3][0]}\n"
        result += f"{self.bCol[4][0]} {self.iCol[4][0]} {self.nCol[4][0]} {self.gCol[4][0]} {self.oCol[4][0]}\n"

        return result

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

        if didFlipBit:
            return winCondition.checkWin(self)
        else:
            return 0

class WinCondition():
    def __init__(self, name, col1, col2, col3, col4, col5):
        self.name = name
        self.col = [col1, col2, col3, col4, col5]

    def __str__(self):
        result = f"{self.name}:\n{self.col[0][0]} {self.col[1][0]} {self.col[2][0]} {self.col[3][0]} {self.col[4][0]}\n"
        result += f"{self.col[0][1]} {self.col[1][1]} {self.col[2][1]} {self.col[3][1]} {self.col[4][1]}\n"
        result += f"{self.col[0][2]} {self.col[1][2]} {self.col[2][2]} {self.col[3][2]} {self.col[4][2]}\n"
        result += f"{self.col[0][3]} {self.col[1][3]} {self.col[2][3]} {self.col[3][3]} {self.col[4][3]}\n"
        result += f"{self.col[0][4]} {self.col[1][4]} {self.col[2][4]} {self.col[3][4]} {self.col[4][4]}\n"

        return result
    
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