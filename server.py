import http.server
import socketserver

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        print(format % args, flush=True)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

PORT = 5000
with ReusableTCPServer(("0.0.0.0", PORT), NoCacheHandler) as httpd:
    print(f"Serving on port {PORT}", flush=True)
    httpd.serve_forever()
