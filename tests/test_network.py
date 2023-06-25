import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from linkcheck.network import check_url


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(405 if self.path == "/fallback" else 404)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args):
        pass


class NetworkTests(unittest.TestCase):
    def test_head_fallback_and_missing(self):
        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = "http://127.0.0.1:%s" % server.server_port
        try:
            self.assertEqual(check_url(base + "/fallback"), (200, None))
            self.assertEqual(check_url(base + "/missing")[0], 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
