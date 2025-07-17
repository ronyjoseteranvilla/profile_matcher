"""
Application entry point for the web service.
"""
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import os

from web.router import player_profile_router


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler class"""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        match = re.match(r"^/get_client_config/([a-fA-F0-9\-]{36})$", path)

        if match:
            player_id = match.group(1)

            try:
                result = player_profile_router.get_player_profile_by_id(
                    player_id)

                if not result:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(
                        "Error: Player Profile not found".encode("utf-8"))
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(result).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Internal error: {e} ".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")


def run_serve():
    """Run localhost serve"""

    host: str = os.getenv("API_HOST", "localhost")
    port: int = int(os.getenv("API_PORT", 8080))
    server_address = (host, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Running serve on {host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_serve()
