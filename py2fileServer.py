import SimpleHTTPServer
import SocketServer
import urlparse
import os
import cgi
from io import StringIO
class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """
            <html>
            <body>
            <h1>File Upload and Download</h1>
            <h2>Upload File</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept="*/*">
                <input type="submit" value="Upload">
            </form>
            <h2>Download Files</h2>
            <ul>
            """
            files = os.listdir(os.getcwd())  
            for file_name in files:
                html += '<li><a href="/download/{}" download>{}</a></li>'.format(file_name, file_name)

            html += """
            </ul>
            </body>
            </html>
            """
            self.wfile.write(html)
        elif self.path.startswith("/download/"):
            file_name = self.path.split("/")[-1]
            file_path = os.path.join(os.getcwd(), file_name)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/octet-stream')
                    self.send_header('Content-Disposition', 'attachment; filename="{}"'.format(file_name))
                    self.end_headers()
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/upload":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            form = cgi.FieldStorage(
                fp=StringIO(post_data),
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
            )

            if 'file' in form:
                file_item = form['file']
                file_name = file_item.filename
                if file_name:
                    file_path = os.path.join(os.getcwd(), file_name)
                    try:
                        with open(file_path, 'wb') as f:
                            f.write(file_item.file.read())
                        self.send_response(302)
                        self.send_header('Location', '/')
                        self.end_headers()
                    except IOError as e:
                        print("Error saving uploaded file:", e)
                        self.send_response(500)
                        self.end_headers()
                else:
                    self.send_response(400)
                    self.end_headers()
            else:
                self.send_response(400)
                self.end_headers()
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
