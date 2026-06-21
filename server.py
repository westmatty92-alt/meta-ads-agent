import http.server
import socketserver
import os

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        self.send_header("ETag", str(os.path.getmtime(self.translate_path(self.path))))
        super().end_headers()

    def log_message(self, format, *args):
        print(format % args, flush=True)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

PORT = 5000
with ReusableTCPServer(("0.0.0.0", PORT), NoCacheHandler) as httpd:
    print(f"Serving on port {PORT}", flush=True)
    httpd.serve_forever()
