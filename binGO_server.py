import binGO_classes
from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

PAGE_HEADER = """<!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                            <style>
                                .circle-container {
                                    width: 200px;
                                    height: 200px;
                                    border-radius: 50%;
                                    background-color: #f0f0f0;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    position: relative;
                                }

                                .input-field {
                                    position: absolute;
                                    width: 80%;
                                    padding: 0.5em;
                                    border-radius: 5px;
                                    border: none;
                                    background-color: #f0f0f0;
                                    text-align: center;
                                    font-size: 16px;
                                }

                                .grid-item {
                                    width: 50px;
                                    height: 50px;
                                    border: 1px solid black;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                }

                                .grid-container {
                                    display: grid;
                                    grid-template-columns: repeat(5, 50px);
                                    grid-template-rows: repeat(5, 50px);
                                    gap: 5px; /* Gap between grid items */
                                }

                                .parent-grid {
                                    display: grid;
                                    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* Automatically adjust columns */
                                    grid-auto-rows: minmax(100px, auto); /* Automatically adjust rows */
                                    gap: 20px;
                                }

                                .item-1 {
                                    background-color: yellow;    
                                }

                                .dropbtn {
                                    background-color: #4CAF50;
                                    color: white;
                                    padding: 16px;
                                    font-size: 16px;
                                    min-width: 160px;
                                    border: none;
                                    cursor: pointer;
                                }

                                .dropdown {
                                    position: relative;
                                    display: inline-block;
                                }

                                .dropdown-content {
                                    display: none;
                                    position: absolute;
                                    background-color: #f9f9f9;
                                    min-width: 160px;
                                    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
                                    z-index: 1;
                                }

                                .dropdown-content div {
                                    color: black;
                                    text-decoration: none;
                                    display: block;
                                }

                                .dropdown-content div:hover {background-color: #f1f1f1}

                                .dropdown:hover .dropdown-content {
                                    display: block;
                                }

                                .dropdown:hover .dropbtn {
                                    background-color: #3e8e41;
                                }
                            </style>
                            <title>BinGO - Play</title>
                        </head>
              """

PAGE_AJAX = f""" <script>
                    $(document).ready(function(){{
                              
                        updateContent();

                        $("#enter-num").click(function(){{
                            updateContent();
                        }});

                        $('#num-input').keypress(function(event) {{
                            if (event.keyCode === 13){{
                                updateContent();
                            }}
                        }});
                    }});

                function editOrDelete(num) {{
                    document.getElementById("change-delete-" + num).submit()
                }}

                function changeWin(name) {{
                    $.ajax({{
                        url: "/binGO_change_win",
                        type: 'POST',
                        data: {{value: name}},
                        success: function(response) {{
                            var dialogBox = document.getElementById('dialogBox');
                            if (dialogBox) {{
                                dialogBox.remove();
                            }}
                            updateContent();
                        }}
                    }});
                }}

                function editOrDeleteWin(name) {{
                    var inputName = document.createElement("input");
                    inputName.setAttribute("type", "hidden");
                    inputName.setAttribute("name", "win-name");
                    inputName.setAttribute("id", "win-name");
                    inputName.setAttribute("value", name);
                    document.getElementById("win-edit-delete-form").appendChild(inputName);
                    document.getElementById("win-edit-delete-form").submit();
                }}

                function updateContent() {{
                    var number = $("#num-input").val();
                    
                    $.ajax({{
                        url: "/binGO_get_cards",
                        type: 'POST',
                        data: {{value: number}},
                        success: function(response) {{
                            $.ajax({{
                                url: "/binGO_get_win_bit",
                                type: 'GET',
                                success: function(response) {{
                                    if (response === '1') {{
                                        $.ajax({{
                                            url: "/binGO_get_back_id",
                                            type: 'GET',
                                            success: function(response) {{
                                                var backID = parseInt(response);

                                                $.ajax({{
                                                    url: "/binGO_get_middle_id",
                                                    type: 'GET',
                                                    success: function(response) {{
                                                        var middleID = parseInt(response);
                                                        var dialog = document.getElementById('dialog');

                                                        if (dialog) {{
                                                            dialog.innerHTML = '<h1>Winner!</h1><h2>Middle ID: ' + middleID + ', Back ID: ' + backID + '</h2>';
                                                        }} else {{
                                                            document.getElementById("hr-tag").insertAdjacentHTML("afterend", "<div id='dialogBox'><dialog id='dialog' open><h1>Winner!</h1><h2>Middle ID: " + middleID + ", Back ID: " + backID + "</dialog><br><br><br><br><br><br><br><br><br><br><div>");
                                                        }}
                                                    }}
                                                }});
                                            }}
                                        }});
                                    }}
                                }}
                            }});
                            $("#num-input").val('');
                            $("#parent-grid").html(response);
                        }}
                    }});
                }}

                </script>"""

class binGoServer(HTTPServer):
    def __init__(self, address, handler):
        self.cards = []
        self.winCondition = binGO_classes.WinCondition("winner", [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1])
        self.winnerCard = None
        self.numbersCalled = []
        super().__init__(address, handler)

class binGoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/' or self.path in ['/binGO_start_page.html']:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_start_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_card_page.html']:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_card_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_win_page.html']:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_win_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_get_win_bit']:
            if self.server.winnerCard is not None:
                returnValue =  1
            else:
                returnValue =  0
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(str(returnValue), "utf-8"))

        elif self.path in ['/binGO_get_middle_id']:
            returnValue = self.server.winnerCard.middleId

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(str(returnValue), "utf-8"))

        elif self.path in ['/binGO_get_back_id']:
            returnValue = self.server.winnerCard.backId

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(str(returnValue), "utf-8"))

    def do_POST(self):
        if self.path in ['/binGO_play.html']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})

            colour = int(form.getvalue('colour'))

            html = PAGE_HEADER

            # 1 = Pink, 2 = Green, 3 = Yellow, 4 = Blue, 5 = Orange
            if colour == 1:
                cardIndexes = db.getCardsByColour("pink")

                if cardIndexes is None:
                    html += """ <body style="background-color: pink;">
                                    <h1>You have no entered cards for Pink. Enter some by clicking on the taskbar, or clicking <a href="binGO_card_page.html">here.</a></h1>
                                    <h1>You can also click <a href="binGO_card_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    cardArray = []
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        cardArray.append(card)
                        self.server.cards = cardArray

                    winNames = db.getAllWinNames()
                    winNamesHTML = ''.join(f"""<div><h3 onclick="changeWin('{name}')">{name}</h3></div>""" for name in winNames)
                    winNamesCDHTML = ''.join(f"""<div><h3 onclick="editOrDeleteWin('{name}')">{name}</h3></div>""" for name in winNames)

                    html += """ <body style="background-color: pink;">
                                    <center>
                                        <form action="/binGO_win_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Win</button>
                                            </div>
                                        </form>"""
                    html +=        f""" <div class="dropdown">
                                            <button class="dropbtn">Apply New Win</button>
                                            <div class="dropdown-content">
                                            {winNamesHTML}
                                            </div>
                                        </div>"""
                    html +=         f"""<form id="win-edit-delete-form" action="/binGO_edit_delete_win.html" method="post" style="display: inline">
                                            <div class="dropdown">
                                                <button class="dropbtn">Edit/Delete Win</button>
                                                <div class="dropdown-content">
                                                {winNamesCDHTML}
                                                </div>
                                            </div>
                                        </form>"""
                    html +=         """ <form action="/binGO_card_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Card</button>
                                            </div>
                                        </form>
                                    </center><br><br>
                                    <div class="circle-container">
                                        <input class="input-field" id="num-input" type="text" value="0"/>
                                    </div>
                                    <button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button id="end-button" type="submit">End Game</button></form><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>"""
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""

            elif colour == 2:
                cardIndexes = db.getCardsByColour("green")

                if cardIndexes is None:
                    html += """ <body style="background-color: green;">
                                    <h1>You have no entered cards for Green. Enter some by clicking on the taskbar, or clicking <a href="binGO_card_page.html">here.</a></h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    cardArray = []
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        cardArray.append(card)
                        self.server.cards = cardArray

                    winNames = db.getAllWinNames()
                    winNamesHTML = ''.join(f"""<div onclick="changeWin('{name}')"><h1>{name}</h1></div>""" for name in winNames)

                    html += """ <body style="background-color: pink;">
                                    <center>
                                        <form action="/binGO_win_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Win</button>
                                            </div>
                                        </form>"""
                    html +=        f""" <div class="dropdown">
                                            <button class="dropbtn">Apply New Win</button>
                                                <div class="dropdown-content">
                                                {winNamesHTML}
                                                </div>
                                        </div>"""
                    html +=         """ <form action="/binGO_card_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Card</button>
                                            </div>
                                        </form>
                                    <center><br>
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>"""
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""
            elif colour == 3:
                cardIndexes = db.getCardsByColour("yellow")

                if cardIndexes is None:
                    html += """ <body style="background-color: #FFD800;">
                                    <h1>You have no entered cards for Yellow. Enter some by clicking on the taskbar, or clicking <a href="binGO_card_page.html">here.</a></h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    cardArray = []
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        cardArray.append(card)
                        self.server.cards = cardArray

                    winNames = db.getAllWinNames()
                    winNamesHTML = ''.join(f"""<div onclick="changeWin('{name}')"><h1>{name}</h1></div>""" for name in winNames)

                    html += """ <body style="background-color: pink;">
                                    <center>
                                        <form action="/binGO_win_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Win</button>
                                            </div>
                                        </form>"""
                    html +=        f""" <div class="dropdown">
                                            <button class="dropbtn">Apply New Win</button>
                                                <div class="dropdown-content">
                                                {winNamesHTML}
                                                </div>
                                        </div>"""
                    html +=         """ <form action="/binGO_card_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Card</button>
                                            </div>
                                        </form>
                                    <center><br>
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>"""
                    
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""

            elif colour == 4:
                cardIndexes = db.getCardsByColour("blue")

                if cardIndexes is None:
                    html += """ <body style="background-color: blue;">
                                    <h1>You have no entered cards for Blue. Enter some by clicking on the taskbar, or clicking <a href="binGO_card_page.html">here.</a></h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    cardArray = []
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        cardArray.append(card)
                        self.server.cards = cardArray

                    winNames = db.getAllWinNames()
                    winNamesHTML = ''.join(f"""<div onclick="changeWin('{name}')"><h1>{name}</h1></div>""" for name in winNames)

                    html += """ <body style="background-color: pink;">
                                    <center>
                                        <form action="/binGO_win_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Win</button>
                                            </div>
                                        </form>"""
                    html +=        f""" <div class="dropdown">
                                            <button class="dropbtn">Apply New Win</button>
                                                <div class="dropdown-content">
                                                {winNamesHTML}
                                                </div>
                                        </div>"""
                    html +=         """ <form action="/binGO_card_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Card</button>
                                            </div>
                                        </form>
                                    <center><br>
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>"""
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""

            else:
                cardIndexes = db.getCardsByColour("orange")

                if cardIndexes is None:
                    html += """ <body style="background-color: orange;">
                                    <h1>You have no entered cards for Orange. Enter some by clicking on the taskbar, or clicking <a href="binGO_card_page.html">here.</a></h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    cardArray = []
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        cardArray.append(card)
                        self.server.cards = cardArray
                        
                    winNames = db.getAllWinNames()
                    winNamesHTML = ''.join(f"""<div onclick="changeWin('{name}')"><h1>{name}</h1></div>""" for name in winNames)

                    html += """ <body style="background-color: pink;">
                                    <center>
                                        <form action="/binGO_win_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Win</button>
                                            </div>
                                        </form>"""
                    html +=        f""" <div class="dropdown">
                                            <button class="dropbtn">Apply New Win</button>
                                                <div class="dropdown-content">
                                                {winNamesHTML}
                                                </div>
                                        </div>"""
                    html +=         """ <form action="/binGO_card_page.html" method="post" style="display: inline;">
                                            <div class="dropdown">
                                                <button class="dropbtn" type="submit">Create New Card</button>
                                            </div>
                                        </form>
                                    <center><br>
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>"""
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(bytes(html, "utf-8"))

        elif self.path in ['/binGO_get_cards']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})

            if form.getvalue("value") is None:
                num = 0
            else:
                num = int(form.getvalue("value"))

            self.server.numbersCalled.append(num)

            cardHtml = ""
            i = 1
            for card in self.server.cards:
                win = card.flipTileBit(num, self.server.winCondition)

                if win == 1:
                    self.server.winnerCard = card

                cardHtml += f"""<form id="change-delete-{i}" action="binGO_edit_delete_card.html" method="post">
                                <input type="hidden" id="card-num" name="card-num" value="{i}"/>
                                <div onclick="editOrDelete('{i}')" class="grid-container">"""
                cardHtml += f"""<div class="grid-item item-{card.bCol[0][1]}">{card.bCol[0][0]}</div>
                            <div class="grid-item item-{card.iCol[0][1]}">{card.iCol[0][0]}</div>
                            <div class="grid-item item-{card.nCol[0][1]}">{card.nCol[0][0]}</div>
                            <div class="grid-item item-{card.gCol[0][1]}">{card.gCol[0][0]}</div>
                            <div class="grid-item item-{card.oCol[0][1]}">{card.oCol[0][0]}</div>
                            <div class="grid-item item-{card.bCol[1][1]}">{card.bCol[1][0]}</div>
                            <div class="grid-item item-{card.iCol[1][1]}">{card.iCol[1][0]}</div>
                            <div class="grid-item item-{card.nCol[1][1]}">{card.nCol[1][0]}</div>
                            <div class="grid-item item-{card.gCol[1][1]}">{card.gCol[1][0]}</div>
                            <div class="grid-item item-{card.oCol[1][1]}">{card.oCol[1][0]}</div>
                            <div class="grid-item item-{card.bCol[2][1]}">{card.bCol[2][0]}</div>
                            <div class="grid-item item-{card.iCol[2][1]}">{card.iCol[2][0]}</div>
                            <div class="grid-item item-{card.nCol[2][1]}">FREE</div>
                            <div class="grid-item item-{card.gCol[2][1]}">{card.gCol[2][0]}</div>
                            <div class="grid-item item-{card.oCol[2][1]}">{card.oCol[2][0]}</div>
                            <div class="grid-item item-{card.bCol[3][1]}">{card.bCol[3][0]}</div>
                            <div class="grid-item item-{card.iCol[3][1]}">{card.iCol[3][0]}</div>
                            <div class="grid-item item-{card.nCol[3][1]}">{card.nCol[3][0]}</div>
                            <div class="grid-item item-{card.gCol[3][1]}">{card.gCol[3][0]}</div>
                            <div class="grid-item item-{card.oCol[3][1]}">{card.oCol[3][0]}</div>
                            <div class="grid-item item-{card.bCol[4][1]}">{card.bCol[4][0]}</div>
                            <div class="grid-item item-{card.iCol[4][1]}">{card.iCol[4][0]}</div>
                            <div class="grid-item item-{card.nCol[4][1]}">{card.nCol[4][0]}</div>
                            <div class="grid-item item-{card.gCol[4][1]}">{card.gCol[4][0]}</div>
                            <div class="grid-item item-{card.oCol[4][1]}">{card.oCol[4][0]}</div>"""
                cardHtml += "</div></form>"
                i += 1

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(cardHtml, "utf-8"))

        elif self.path in ['/binGO_card_page.html']:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_card_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_win_page.html']:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_win_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_submit_card.html']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})
            bCol = [int(form.getvalue('B1')), int(form.getvalue('B2')), int(form.getvalue('B3')), int(form.getvalue('B4')), int(form.getvalue('B5'))]
            iCol = [int(form.getvalue('I1')), int(form.getvalue('I2')), int(form.getvalue('I3')), int(form.getvalue('I4')), int(form.getvalue('I5'))]
            nCol = [int(form.getvalue('N1')), int(form.getvalue('N2')), 0, int(form.getvalue('N4')), int(form.getvalue('N5'))]
            gCol = [int(form.getvalue('G1')), int(form.getvalue('G2')), int(form.getvalue('G3')), int(form.getvalue('G4')), int(form.getvalue('G5'))]
            oCol = [int(form.getvalue('O1')), int(form.getvalue('O2')), int(form.getvalue('O3')), int(form.getvalue('O4')), int(form.getvalue('O5'))]

            card = binGO_classes.Card(form.getvalue('colour'), int(form.getvalue('id1')), int(form.getvalue('id2')), bCol, iCol, nCol, gCol, oCol)
            db.readCard(card)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("binGO_pages/binGO_start_page.html", "rb") as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_submit_win.html']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})
            bCol = [int(form.getvalue('B1')), int(form.getvalue('B2')), int(form.getvalue('B3')), int(form.getvalue('B4')), int(form.getvalue('B5'))]
            iCol = [int(form.getvalue('I1')), int(form.getvalue('I2')), int(form.getvalue('I3')), int(form.getvalue('I4')), int(form.getvalue('I5'))]
            nCol = [int(form.getvalue('N1')), int(form.getvalue('N2')), int(form.getvalue('N3')), int(form.getvalue('N4')), int(form.getvalue('N5'))]
            gCol = [int(form.getvalue('G1')), int(form.getvalue('G2')), int(form.getvalue('G3')), int(form.getvalue('G4')), int(form.getvalue('G5'))]
            oCol = [int(form.getvalue('O1')), int(form.getvalue('O2')), int(form.getvalue('O3')), int(form.getvalue('O4')), int(form.getvalue('O5'))]

            winCondition = binGO_classes.WinCondition(form.getvalue('name'), bCol, iCol, nCol, gCol, oCol)
            db.readWin(winCondition)
            self.server.winCondition = winCondition

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("binGO_pages/binGO_start_page.html", "rb") as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_end_game.html']:
            self.server.cards = []
            self.server.winnerCard = None
            self.server.numbersCalled = []

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("binGO_pages/binGO_start_page.html", "rb") as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_change_win']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})

            name = form.getvalue("value")

            self.server.winCondition = db.writeWin(db.getWinIdByName(name))
            self.server.winnerCard = None
            nameOfWin = self.server.winCondition.name

            for card in self.server.cards:
                card.reapplyWin(self.server.winCondition, self.server.numbersCalled)

            self.send_response(200)
            self.end_headers()

            self.wfile.write(bytes(nameOfWin, "utf-8"))

        elif self.path in ['/binGO_edit_delete_card.html']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})

            cardNum = int(form.getvalue("card-num"))
            card = db.writeCard(cardNum)
            
            html = f""" <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>BinGO - Enter New Card</title>
                            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                            <style>
                                .grid {{
                                    display: grid;
                                    grid-template-columns: repeat(5, 100px);
                                    grid-template-rows: repeat(6, 100px);
                                    gap: 1px;
                                    justify-content: center;
                                    align-items: center;
                                }}

                                .grid-item {{
                                    width: 100px;
                                    height: 100px;
                                    border: 1px black;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                }}

                                .input-box {{
                                    font-size: 50px;
                                    text-align: center;
                                }}
                            </style>
                            <script>
                                function changeCard() {{
                                    document.getElementById("change-form").submit();
                                }}

                                function deleteCard() {{
                                    document.getElementById("delete-form").submit();
                                }}
                            </script>
                        </head>
                        <body style="background-color: rgb(4, 22, 108);">
                            <center>
                                <form id="change-form" action="binGO_change_card" method="post">
                                    <input type="hidden" id="card-num" name="card-num" value="{cardNum}"/>
                                    <div class="card-extras">
                                        <select id="colour" name="colour">
                                            <option value="pink">Pink</option>
                                            <option value="green">Green</option>
                                            <option value="yellow">Yellow</option>
                                            <option value="blue">Blue</option>
                                            <option value="orange">Orange</option> 
                                        </select>
                                        <input value="{card.middleId}"id="id1" name="id1" type="number" required/>
                                        <input value="{card.backId}" id="id2" name="id2" type="number" required/>
                                    </div>
                                    <div class="grid">
                                        <div class="grid-item" style="font-size: 50px; text-align: center; background-color: aqua;">B</div>
                                        <div class="grid-item" style="font-size: 50px; text-align: center; background-color: aqua;">I</div>
                                        <div class="grid-item" style="font-size: 50px; text-align: center; background-color: aqua;">N</div>
                                        <div class="grid-item" style="font-size: 50px; text-align: center; background-color: aqua;">G</div>
                                        <div class="grid-item" style="font-size: 50px; text-align: center; background-color: aqua;">O</div>
                                        <input value="{card.bCol[0][0]}" id="B1" name="B1" type="number" class=" input-box" min="1" max="15"/>
                                        <input value="{card.iCol[0][0]}" id="I1" name="I1" type="number" class=" input-box" min="16" max="30"/>
                                        <input value="{card.nCol[0][0]}" id="N1" name="N1" type="number" class=" input-box" min="31" max="45"/>
                                        <input value="{card.gCol[0][0]}" id="G1" name="G1" type="number" class=" input-box" min="46" max="60"/>
                                        <input value="{card.oCol[0][0]}" id="O1" name="O1" type="number" class=" input-box" min="61" max="75"/>
                                        <input value="{card.bCol[1][0]}" id="B2" name="B2" type="number" class=" input-box" min="1" max="15"/>
                                        <input value="{card.iCol[1][0]}" id="I2" name="I2" type="number" class=" input-box" min="16" max="30"/>
                                        <input value="{card.nCol[1][0]}" id="N2" name="N2" type="number" class=" input-box" min="31" max="45"/>
                                        <input value="{card.gCol[1][0]}" id="G2" name="G2" type="number" class=" input-box" min="46" max="60"/>
                                        <input value="{card.oCol[1][0]}" id="O2" name="O2" type="number" class=" input-box" min="61" max="75"/>
                                        <input value="{card.bCol[2][0]}" id="B3" name="B3" type="number" class=" input-box" min="1" max="15"/>
                                        <input value="{card.iCol[2][0]}" id="I3" name="I3" type="number" class=" input-box" min="16" max="30"/>
                                        <div class="grid-item" style="background-color: white;">Free Space</div>
                                        <input value="{card.gCol[2][0]}" id="G3" name="G3" type="number" class=" input-box" min="46" max="60"/>
                                        <input value="{card.oCol[2][0]}" id="O3" name="O3" type="number" class=" input-box" min="61" max="75"/>
                                        <input value="{card.bCol[3][0]}" id="B4" name="B4" type="number" class=" input-box" min="1" max="15"/>
                                        <input value="{card.iCol[3][0]}" id="I4" name="I4" type="number" class=" input-box" min="16" max="30"/>
                                        <input value="{card.nCol[3][0]}" id="N4" name="N4" type="number" class=" input-box" min="31" max="45"/>
                                        <input value="{card.gCol[3][0]}" id="G4" name="G4" type="number" class=" input-box" min="46" max="60"/>
                                        <input value="{card.oCol[3][0]}" id="O4" name="O4" type="number" class=" input-box" min="61" max="75"/>
                                        <input value="{card.bCol[4][0]}" id="B5" name="B5" type="number" class=" input-box" min="1" max="15"/>
                                        <input value="{card.iCol[4][0]}" id="I5" name="I5" type="number" class=" input-box" min="16" max="30"/>
                                        <input value="{card.nCol[4][0]}" id="N5" name="N5" type="number" class=" input-box" min="31" max="45"/>
                                        <input value="{card.gCol[4][0]}" id="G5" name="G5" type="number" class=" input-box" min="46" max="60"/>
                                        <input value="{card.oCol[4][0]}" id="O5" name="O5" type="number" class=" input-box" min="61" max="75"/>
                                    </div>
                                </form>
                                <form id="delete-form" action="binGO_delete_card" method="post">
                                    <input type="hidden" id="d-card-num" name="d-card-num" value="{cardNum}"/>
                                </form>
                                <button onclick="changeCard()">Change</button>
                                <button onclick="deleteCard()">Delete</button>
                             </center>
                        </body>
                        </html>"""
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))

        elif self.path in ['/binGO_change_card']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})

            bCol = f"{form.getvalue('B1')},{form.getvalue('B2')},{form.getvalue('B3')},{form.getvalue('B4')},{form.getvalue('B5')}"
            iCol = f"{form.getvalue('I1')},{form.getvalue('I2')},{form.getvalue('I3')},{form.getvalue('I4')},{form.getvalue('I5')}"
            nCol = f"{form.getvalue('N1')},{form.getvalue('N2')},0,{form.getvalue('N4')},{form.getvalue('N5')}"
            gCol = f"{form.getvalue('G1')},{form.getvalue('G2')},{form.getvalue('G3')},{form.getvalue('G4')},{form.getvalue('G5')}"
            oCol = f"{form.getvalue('O1')},{form.getvalue('O2')},{form.getvalue('O3')},{form.getvalue('O4')},{form.getvalue('O5')}"

            db.changeCard(int(form.getvalue("card-num")), int(form.getvalue("id1")), int(form.getvalue("id2")), bCol, iCol, nCol, gCol, oCol)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_start_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_delete_card']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})
            
            db.deleteCard(int(form.getvalue("d-card-num")))

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_start_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_edit_delete_win.html']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})

            winName = form.getvalue("win-name")
            winId = db.getWinIdByName(winName)
            win = db.writeWin(winId)

            html = f"""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
                    body {{
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        background: #27282c;
                        font-family: 'Poppins', sans-serif;
                        overflow: hidden;
                    }}

                    .container {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                    }}

                    .grid-container {{
                        display: grid;
                        grid-template-columns: repeat(5, 100px);
                        grid-template-rows: repeat(5, 100px);
                        gap: 5px;
                        border: 3px solid white;
                        padding: 5px;
                    }}

                
                    a {{
                        position: relative;
                        background: white;
                        color: white;
                        text-decoration: none;
                        text-transform: uppercase;
                        font-size: 1.5em;
                        letter-spacing: 0.1em;
                        font-weight: 400;
                        padding: 5px 30px;
                        transition: 0.5s;
                    }}

                    a:hover {{
                        letter-spacing: 0.25em;
                        background: var(--clr);
                        color: var(--clr);
                        box-shadow: 0 0 35px var(--clr);
                    }}

                    a:before {{
                        content: '';
                        position: absolute;
                        inset: 2px;
                        background: #27282c;
                    }}

                    a span {{
                        position: relative;
                        z-index: 1;
                    }}

                    label {{
                        color: whitesmoke;
                        text-shadow: 2px 2px 4px black;
                        text-align: center;
                        font-size: 30px;
                    }}

                    .name-of-win {{
                        font-size: 30px;
                        background-color: #27282c;
                        color: whitesmoke;
                    }}

                    .button-holder {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        width: 100%;
                    }}

                    .grid-item-1 {{
                        background: darkblue;
                        border: 3px solid white;
                    }}

                    .grid-item-0 {{
                        background: slategrey;
                        border: 3px solid white;
                    }}

                </style>
                <title>BinGO - Enter New Win</title>
            </head>
            <body>
                <form id="change-form" action="binGO_edit_win" method="post">
                    <input id="win-id" name="win-id" type="hidden" value="{winId}"/>
                    <input id="B1" name="B1" type="hidden" value="{win.col[0][0]}"/>
                    <input id="I1" name="I1" type="hidden" value="{win.col[1][0]}"/>
                    <input id="N1" name="N1" type="hidden" value="{win.col[2][0]}"/>
                    <input id="G1" name="G1" type="hidden" value="{win.col[3][0]}"/>
                    <input id="O1" name="O1" type="hidden" value="{win.col[4][0]}"/>
                    <input id="B2" name="B2" type="hidden" value="{win.col[0][1]}"/>
                    <input id="I2" name="I2" type="hidden" value="{win.col[1][1]}"/>
                    <input id="N2" name="N2" type="hidden" value="{win.col[2][1]}"/>
                    <input id="G2" name="G2" type="hidden" value="{win.col[3][1]}"/>
                    <input id="O2" name="O2" type="hidden" value="{win.col[4][1]}"/>
                    <input id="B3" name="B3" type="hidden" value="{win.col[0][2]}"/>
                    <input id="I3" name="I3" type="hidden" value="{win.col[1][2]}"/>
                    <input id="N3" name="N3" type="hidden" value="{win.col[2][2]}"/>
                    <input id="G3" name="G3" type="hidden" value="{win.col[3][2]}"/>
                    <input id="O3" name="O3" type="hidden" value="{win.col[4][2]}"/>
                    <input id="B4" name="B4" type="hidden" value="{win.col[0][3]}"/>
                    <input id="I4" name="I4" type="hidden" value="{win.col[1][3]}"/>
                    <input id="N4" name="N4" type="hidden" value="{win.col[2][3]}"/>
                    <input id="G4" name="G4" type="hidden" value="{win.col[3][3]}"/>
                    <input id="O4" name="O4" type="hidden" value="{win.col[4][3]}"/>
                    <input id="B5" name="B5" type="hidden" value="{win.col[0][4]}"/>
                    <input id="I5" name="I5" type="hidden" value="{win.col[1][4]}"/>
                    <input id="N5" name="N5" type="hidden" value="{win.col[2][4]}"/>
                    <input id="G5" name="G5" type="hidden" value="{win.col[3][4]}"/>
                    <input id="O5" name="O5" type="hidden" value="{win.col[4][4]}"/>
                    <center>
                        <label for="name">Name of Win:</label>
                        <input value="{win.name}" id="name" name="name" type="text"/>
                        <br>
                        <br>
                        <hr>
                        <br>
                    </center>

                    <div class="container">
                        <div class="grid-container">
                            <div class="grid-item-{win.col[0][0]}" onclick="flipTile(this, 'B1')"></div>
                            <div class="grid-item-{win.col[1][0]}" onclick="flipTile(this, 'I1')"></div>
                            <div class="grid-item-{win.col[2][0]}" onclick="flipTile(this, 'N1')"></div>
                            <div class="grid-item-{win.col[3][0]}" onclick="flipTile(this, 'G1')"></div>
                            <div class="grid-item-{win.col[4][0]}" onclick="flipTile(this, 'O1')"></div>
                            <div class="grid-item-{win.col[0][1]}" onclick="flipTile(this, 'B2')"></div>
                            <div class="grid-item-{win.col[1][1]}" onclick="flipTile(this, 'I2')"></div>
                            <div class="grid-item-{win.col[2][1]}" onclick="flipTile(this, 'N2')"></div>
                            <div class="grid-item-{win.col[3][1]}" onclick="flipTile(this, 'G2')"></div>
                            <div class="grid-item-{win.col[4][1]}" onclick="flipTile(this, 'O2')"></div>
                            <div class="grid-item-{win.col[0][2]}" onclick="flipTile(this, 'B3')"></div>
                            <div class="grid-item-{win.col[1][2]}" onclick="flipTile(this, 'I3')"></div>
                            <div class="grid-item-{win.col[2][2]}" onclick="flipTile(this, 'N3')"></div>
                            <div class="grid-item-{win.col[3][2]}" onclick="flipTile(this, 'G3')"></div>
                            <div class="grid-item-{win.col[4][2]}" onclick="flipTile(this, 'O3')"></div>
                            <div class="grid-item-{win.col[0][3]}" onclick="flipTile(this, 'B4')"></div>
                            <div class="grid-item-{win.col[1][3]}" onclick="flipTile(this, 'I4')"></div>
                            <div class="grid-item-{win.col[2][3]}" onclick="flipTile(this, 'N4')"></div>
                            <div class="grid-item-{win.col[3][3]}" onclick="flipTile(this, 'G4')"></div>
                            <div class="grid-item-{win.col[4][3]}" onclick="flipTile(this, 'O4')"></div>
                            <div class="grid-item-{win.col[0][4]}" onclick="flipTile(this, 'B5')"></div>
                            <div class="grid-item-{win.col[1][4]}" onclick="flipTile(this, 'I5')"></div>
                            <div class="grid-item-{win.col[2][4]}" onclick="flipTile(this, 'N5')"></div>
                            <div class="grid-item-{win.col[3][4]}" onclick="flipTile(this, 'G5')"></div>
                            <div class="grid-item-{win.col[4][4]}" onclick="flipTile(this, 'O5')"></div>
                        </div>
                    </div>
                </form>
                <form id="delete-form" action="binGO_delete_win" method="post">
                    <input type="hidden" value="{winId}" name="win-id" id="win-id"/>
                </form>

                <div class="button-holder">
                    <a style="--clr:steelblue" onclick="changeWin()"><span>Change</span></a>
                    <a style="--clr:steelblue" onclick="deleteWin()"><span>Delete</span></a>
                </div>
                <script>
                    function flipTile(element, key) {{
                        var computedStyle = window.getComputedStyle(element);
                        var currentColour = computedStyle.backgroundColor;
                        
                        if (currentColour === 'rgb(112, 128, 144)') {{
                            element.style.backgroundColor = 'darkblue';
                            document.getElementById(key).value = 1;
                        }} else {{
                            element.style.backgroundColor = 'rgb(112, 128, 144)';
                            document.getElementById(key).value = 0
                        }}
                    }}

                    function changeWin() {{
                        document.getElementById("change-form").submit();
                    }}

                    function deleteWin() {{
                        document.getElementById("delete-form").submit();
                    }}
                </script>
            </body>
            </html>"""

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))

        elif self.path in ['/binGO_edit_win']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})

            bCol = f"{form.getvalue('B1')},{form.getvalue('B2')},{form.getvalue('B3')},{form.getvalue('B4')},{form.getvalue('B5')}"
            iCol = f"{form.getvalue('I1')},{form.getvalue('I2')},{form.getvalue('I3')},{form.getvalue('I4')},{form.getvalue('I5')}"
            nCol = f"{form.getvalue('N1')},{form.getvalue('N2')},{form.getvalue('N3')},{form.getvalue('N4')},{form.getvalue('N5')}"
            gCol = f"{form.getvalue('G1')},{form.getvalue('G2')},{form.getvalue('G3')},{form.getvalue('G4')},{form.getvalue('G5')}"
            oCol = f"{form.getvalue('O1')},{form.getvalue('O2')},{form.getvalue('O3')},{form.getvalue('O4')},{form.getvalue('O5')}"

            db.changeWin(int(form.getvalue("win-id")), form.getvalue("name"), bCol, iCol, nCol, gCol, oCol)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_start_page.html', 'rb') as f:
                self.wfile.write(f.read())

        elif self.path in ['/binGO_delete_win']:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ = { 'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type'],})
            
            id = int(form.getvalue('win-id'))

            db.deleteWin(id)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_start_page.html', 'rb') as f:
                self.wfile.write(f.read())

if __name__ == "__main__":
    db = binGO_classes.Database()
    httpd = binGoServer(('localhost', 8000), binGoHandler)
    httpd.serve_forever()