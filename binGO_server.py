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
                                    overflow: auto;
                                }

                                .item-1 {
                                    background-color: yellow;    
                                }
                            </style>
                            <title>BinGO!</title>
                        </head>
              """

PAGE_AJAX = """ <script>
                    $(document).ready(function(){
                        
                        updateContent();

                        $("#enter-num").click(function(){
                            updateContent();
                        });

                        $('#num-input').keypress(function(event) {
                            if (event.keyCode === 13){
                                updateContent();
                            }
                        })

                        function updateContent() {
                            var number = $("#num-input").val();

                            $.ajax({
                                url: "/binGO_get_cards",
                                type: 'POST',
                                data: {value: number},
                                success: function(response) {
                                    $("#num-input").val('');
                                    $("#parent-grid").html(response);
                                }
                            });
                        }
                    });
                </script>"""

class binGoServer(HTTPServer):
    def __init__(self, address, handler):
        self.cards = []
        self.winCondition = binGO_classes.WinCondition("winner", [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1], [1,1,1,1,1])
        super().__init__(address, handler)

class binGoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/' or self.path in ['/binGO_start_page.html']:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_start_page.html', 'rb') as f:
                self.wfile.write(f.read())

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
                                    <h1>You have no entered cards for Pink. Enter some by clicking on the taskbar, or clicking here.</h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        self.server.cards.append(card)

                    html += """ <body style="background-color: pink;">
                                    <center><input id="num-input" type="number"/><button id="enter-num">Submit</button></center><hr>
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""

            elif colour == 2:
                cardIndexes = db.getCardsByColour("green")

                if cardIndexes is None:
                    html += """ <body style="background-color: green;">
                                    <h1>You have no entered cards for Green. Enter some by clicking on the taskbar, or clicking here.</h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        self.server.cards.append(card)

                    html += """ <body style="background-color: green;">
                                    <center><input id="num-input" type="number"/><button id="enter-num">Submit</button></center><hr>
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""
            elif colour == 3:
                cardIndexes = db.getCardsByColour("yellow")

                if cardIndexes is None:
                    html += """ <body style="background-color: #FFD800;">
                                    <h1>You have no entered cards for Yellow. Enter some by clicking on the taskbar, or clicking here.</h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        self.server.cards.append(card)

                    html += """ <body style="background-color: #FFD800;">
                                    <center><input id="num-input" type="number"/><button id="enter-num">Submit</button></center><hr>
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""

            elif colour == 4:
                cardIndexes = db.getCardsByColour("blue")

                if cardIndexes is None:
                    html += """ <body style="background-color: blue;">
                                    <h1>You have no entered cards for Blue. Enter some by clicking on the taskbar, or clicking here.</h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        self.server.cards.append(card)

                    html += """ <body style="background-color: blue;">
                                    <center><input id="num-input" type="number"/><button id="enter-num">Submit</button></center><hr>
                                    <div id="parent-grid" class="parent-grid">init</div>
                            """
                    html += PAGE_AJAX
                    html += """ </body>
                                </html>"""

            else:
                cardIndexes = db.getCardsByColour("orange")

                if cardIndexes is None:
                    html += """ <body style="background-color: orange;">
                                    <h1>You have no entered cards for Orange. Enter some by clicking on the taskbar, or clicking here.</h1>
                                    <h1>You can also click <a href="binGO_start_page.html">here</a> to return to the main menu.</h1>
                                </body>
                            </html>"""
                else:
                    for index in cardIndexes:
                        card = db.writeCard(index)
                        self.server.cards.append(card)

                    html += """ <body style="background-color: orange;">
                                    <center><input id="num-input" type="number"/><button id="enter-num">Submit</button></center><hr>
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

            html = ""
            for card in self.server.cards:
                if num != 0:
                    win = card.flipTileBit(num, self.server.winCondition)
                html += """<div class="grid-container">"""
                html += f"""<div class="grid-item item-{card.bCol[0][1]}">{card.bCol[0][0]}</div>
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
                            <div class="grid-item item-{card.nCol[2][1]}">{card.nCol[2][0]}</div>
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
                html += "</div>"

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(html, "utf-8"))

        elif self.path in ['/binGO_card_page.html']:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                with open('binGO_card_page.html', 'rb') as f:
                    self.wfile.write(f.read())

if __name__ == "__main__":
    db = binGO_classes.Database()
    card = binGO_classes.Card("pink", 888, 8800, [1,2,3,4,5], [16,17,18,19,20], [31,32,33,34,35], [46,47,48,49,50], [61,62,63,64,65])
    card2 = binGO_classes.Card("orange", 888, 8800, [1,2,3,4,5], [16,17,18,19,20], [31,32,33,34,35], [46,47,48,49,50], [61,62,63,64,65])
    db.readCard(card)
    db.readCard(card2)
    httpd = binGoServer(('localhost', 8000), binGoHandler)
    httpd.serve_forever()