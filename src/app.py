"""
Application entry point for the web service.
"""
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import os

from web.router import player_profile_router
from web.dtos.player_profile_models import ClientConfig
from web.repository.player_profile_repository import PlayerProfileNotFoundException


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler class"""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        match = re.match(r"^/get_client_config/([a-fA-F0-9\-]{36})$", path)
        status_code = 200
        response = ""

        if match:
            player_id = match.group(1)

            try:
                result: ClientConfig = player_profile_router.get_client_config_by_id(
                    player_id)

                status_code = 200
                response = result.model_dump_json().encode("utf-8")

            except PlayerProfileNotFoundException as e:
                status_code = 404
                response = e.message.encode("utf-8")

            except Exception as e:
                status_code = 500
                response = f"Internal error: {e} ".encode("utf-8")
        else:
            status_code = 404
            response = f"Endpoint {path} Not Found"

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)


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
