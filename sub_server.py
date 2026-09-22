import base64
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 8000
SECRET_PATH = "/sub"

# Base configuration hosts
SNI_HOST = "firebaseremoteconfigrealtime.googleapis.com"
GRPC_SNI_HOST = "firebase-settings.crashlytics.com"
TARGET_PORT = 443

# Exact SSH link (kept unchanged)
EXACT_SSH_LINK = (
    "ssh://kekz:kekz@firebaseremoteconfigrealtime.googleapis.com:443"
    "?KUX3sw04Vw3D4VZXnUUdx5w2olLTqhuGQNU7herX/y1+G4NHVbZAqskX3V0NNf7dkKWRsCBsXTG3qdxBQSwIR0KXvgghi4/TuvAbQewO0dbGcjBge8N2rucYKV4UuKxEBQWWzGpxciQxmDWGIc00StcC7akqRnZiG0Otw8p3B9dgqNlqwJy2yiI4kQh9I+ERB6KbVUEUJ4e5B/gfpP+RVN5RQTBG7DFl76G6HrScTEkdcQfS0KbeRF9IiyDzuWiBee/UtI6LsEg610E5CG6CjnVBzmtF8kAGRrwEuGhO5UbtTXRfWUCl6QQJ/eH1YaIKHU+OeJvDU6KxGahdJxDCu3KAD+ytdTFDFXFBF7HkNnj1u2y6eoxT286JTl0YeZ9ohrbCc6FeOmpTkwYETA1Pdv4ll0UUkhJQ3WpKGY5ct1+ZZm8611QCwh0UazItWQAyqMMgHKRsGwU7PPRymBqNnmP3isR0umXlyNagFQNXWcav2twr7Nm8xqhRyWCPgpk5ERD6QpLTP/hARnG8mLSAqvJn8yobwY5uzxvCvUNY3D0uKT13pqXyc7ZS3rLT524oouDHRHB7oU7eQBFwAcLvYeQeh5RTBCRn8tkZ9UANkU8HQ73HKh8bj32egC8vPKDzZMIcdKbssjUUr4Q2FsBrGpc/O3wVs+pBbD+g2zkxokrPCJn8GCi4K0+KxbCULhxSg3K2NJXQH8xwvwWQco/oyR1SRLhUB2tY29+UcnSx7eWZNFbvymTcD9E07kSxEqF9BljuT8yjntYCPxE9lkI8xQFWekoSxYVx//lMpMtdA7o=#ssh-ws"
)

def extract_run_app_host(host_header):
    """Extracts host without port from HTTP Host header for host/authority."""
    if host_header:
        return host_header.split(':')[0]
    return "127.0.0.1"

def generate_subscription(host_header):
    run_app_host = extract_run_app_host(host_header)

    # WS Links
    trojan_ws = (
        f"trojan://kekz69@{SNI_HOST}:{TARGET_PORT}"
        f"?type=ws&headerType=none&path=%2FKekzTRWS&security=tls"
        f"&host={run_app_host}&sni={SNI_HOST}#trojan-ws"
    )
    vless_ws = (
        f"vless://kekz69@{SNI_HOST}:{TARGET_PORT}"
        f"?encryption=none&type=ws&headerType=none&path=%2FKekzVLWS&security=tls"
        f"&host={run_app_host}&sni={SNI_HOST}#vless-ws"
    )

    # XHTTP Links
    trojan_xhttp = (
        f"trojan://Kekz69@{SNI_HOST}:{TARGET_PORT}"
        f"?type=xhttp&headerType=packet-up&path=%2FKekzTRXH&security=tls"
        f"&host={run_app_host}&sni={SNI_HOST}#trojan-xhttp(%20auto%20%26%20packet-up%20only%20)"
    )
    vless_xhttp = (
        f"vless://kekz69@{SNI_HOST}:{TARGET_PORT}"
        f"?encryption=none&type=xhttp&headerType=packet-up&path=%2FKekzVLXH&security=tls"
        f"&host={run_app_host}&sni={SNI_HOST}#vless-xhttp(%20auto%20%26%20packet-up%20only%20)"
    )

    # gRPC Links (authority dynamically set to .run.app host)
    trojan_grpc = (
        f"trojan://Kekz69@{GRPC_SNI_HOST}:{TARGET_PORT}"
        f"?mode=gun&security=tls&insecure=0&type=grpc&serviceName=kekz-trojan-grpc"
        f"&allowInsecure=0&authority={run_app_host}&sni={GRPC_SNI_HOST}#trojan-grpc"
    )
    vless_grpc = (
        f"vless://kekz69@{GRPC_SNI_HOST}:{TARGET_PORT}"
        f"?mode=gun&security=tls&encryption=none&insecure=0&type=grpc&serviceName=kekz-vless-grpc"
        f"&allowInsecure=0&authority={run_app_host}&sni={GRPC_SNI_HOST}#vless-grpc"
    )

    # Combine all links into the payload
    raw_payload = (
        f"{EXACT_SSH_LINK}\n"
        f"{trojan_ws}\n"
        f"{vless_ws}\n"
        f"{trojan_xhttp}\n"
        f"{vless_xhttp}\n"
        f"{trojan_grpc}\n"
        f"{vless_grpc}\n"
    )
    return base64.b64encode(raw_payload.encode('utf-8'))

class SubHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        host_header = self.headers.get('Host', '')
        
        if self.path == SECRET_PATH or self.path.startswith(f"{SECRET_PATH}?"):
            sub_body = generate_subscription(host_header)
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Subscription-Userinfo', 'upload=0; download=0; total=107374182400; expire=0')
            self.send_header('Profile-Update-Interval', '24')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            self.wfile.write(sub_body)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def log_message(self, format, *args):
        return

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', PORT), SubHandler)
    print(f"Subscription server running on port {PORT}...")
    server.serve_forever()
