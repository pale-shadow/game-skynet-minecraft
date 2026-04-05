import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from skynet_core import setup_logging
from skynet_process import get_hailo_structure_logic, get_node_logic

logger = setup_logging("skynet_agent")


class SkynetAgentHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/infer":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode("utf-8"))

            logger.info(f"🧠 Received inference request: {params}")

            # Identify which logic to run
            node_type = params.get("node", "node_hailo")
            sector = params.get("sector", "Shroomville")

            if node_type == "void_tech":
                commands = get_hailo_structure_logic(sector=sector)
            else:
                commands = get_node_logic(node=node_type, sector=sector)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"commands": commands}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


def run_agent(port=5000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, SkynetAgentHandler)
    logger.info(f"📡 Skynet Agent listening on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run_agent()
