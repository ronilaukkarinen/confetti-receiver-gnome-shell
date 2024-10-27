from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
from datetime import datetime

class ConfettiRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Confetti triggered")

        # Log confetti trigger with 🎉 emoji
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🎉 Confetti triggered at {now}")

        # Command to enable the GNOME confetti extension
        subprocess.run(["gnome-extensions", "enable", "confetti@ronilaukkarinen"])

        # Optional: Disable after a few seconds to stop the confetti effect
        subprocess.run(["sleep", "5"])
        subprocess.run(["gnome-extensions", "disable", "confetti@ronilaukkarinen"])

    def log_message(self, format, *args):
        return  # Suppress default HTTP logging

def run(server_class=HTTPServer, handler_class=ConfettiRequestHandler, port=4769):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting confetti trigger server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
