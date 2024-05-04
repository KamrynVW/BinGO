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
                            </style>
                            <title>BinGO!</title>
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
                        }})

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

                                                                document.getElementById("hr-tag").insertAdjacentHTML("afterend", "<dialog open><h1>Winner!</h1><h2>Middle ID: " + middleID + ", Back ID: " + backID + "</dialog><br><br><br><br><br><br><br><br><br><br>");
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
                    }});
                </script>"""

class binGoServer(HTTPServer):
    def __init__(self, address, handler):
        self.cards = []
        self.winCondition = binGO_classes.WinCondition("winner", [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1])
        self.winnerCard = None
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
                    if len(self.server.cards) == 0:
                        for index in cardIndexes:
                            card = db.writeCard(index)
                            self.server.cards.append(card)

                    html += """ <body style="background-color: pink;">
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
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
                    if len(self.server.cards) == 0:
                        for index in cardIndexes:
                            card = db.writeCard(index)
                            self.server.cards.append(card)

                    html += """ <body style="background-color: green;">
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
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
                    if len(self.server.cards) == 0:
                        for index in cardIndexes:
                            card = db.writeCard(index)
                            self.server.cards.append(card)

                    html += """ <body style="background-color: #FFD800;">
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
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
                    if len(self.server.cards) == 0:
                        for index in cardIndexes:
                            card = db.writeCard(index)
                            self.server.cards.append(card)

                    html += """ <body style="background-color: blue;">
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
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
                    if len(self.server.cards) == 0:
                        for index in cardIndexes:
                            card = db.writeCard(index)
                            self.server.cards.append(card)

                    html += """ <body style="background-color: orange;">
                                    <center><input id="num-input" type="number" value="0"/><button id="enter-num">Submit</button><form action="/binGO_end_game.html" method="post"><button type="submit">End Game</button></form></center><hr id="hr-tag">
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
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

            cardHtml = ""
            for card in self.server.cards:
                win = card.flipTileBit(num, self.server.winCondition)

                if win == 1:
                    self.server.winnerCard = card

                cardHtml += """<div class="grid-container">"""
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
                cardHtml += "</div>"

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

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("binGO_pages/binGO_start_page.html", "rb") as f:
                self.wfile.write(f.read())

if __name__ == "__main__":
    db = binGO_classes.Database()
    httpd = binGoServer(('localhost', 8000), binGoHandler)
    httpd.serve_forever()