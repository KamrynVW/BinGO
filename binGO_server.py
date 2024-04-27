from binGO_classes import Card
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class binGoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open('binGO_pages/binGO_start_page.html', 'rb') as f:
                self.wfile.write(f.read())

if __name__ == "__main__":
    httpd = HTTPServer(('localhost', 8000), binGoHandler)
    httpd.serve_forever()