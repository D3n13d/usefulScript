import SimpleHTTPServer
import SocketServer
import urlparse

history = []


class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        global history

        if self.path == "/":

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <body>
            <h1>Input Text</h1>
            <form action="/add" method="get">
                <input type="text" name="user_input">
                <input type="submit" value="Submit">
            </form>
            </body>
            </html>
            """
            self.wfile.write(html)
        elif self.path.startswith("/add?user_input="):
        
            user_input = self.path.split("=")[1]
            if user_input:
                history.append(user_input)
            self.send_response(302)  
            self.send_header('Location', '/')  
            self.end_headers()
        elif self.path == "/history":
   
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <body>
            <h1>History</h1>
            <ul>
            """
            for item in history:
                html += "<li>" + item + "</li>"
            html += """
            </ul>
            <a href="/">Go back</a>
            </body>
            </html>
            """
            self.wfile.write(html)
        else:

            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    PORT = 9999
    Handler = CustomHandler

    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "Server started on port", PORT

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "Shutting down the server"
        httpd.shutdown()