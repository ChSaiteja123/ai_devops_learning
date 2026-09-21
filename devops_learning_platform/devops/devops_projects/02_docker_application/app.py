from http.server import BaseHTTPRequestHandler, HTTPServer


class ApplicationHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = b"DevOps application is running\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), ApplicationHandler).serve_forever()
