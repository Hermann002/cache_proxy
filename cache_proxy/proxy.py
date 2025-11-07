import http.server
import threading
from typing import Any
from .cache import get, set
from .forwarder import forward_request
from .utils import sanitize_headers, log_request

class CachingProxyHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, origin_url: str, **kwargs):
        self.origin_url =origin_url.rstrip("/")
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        cache_key = self.path
        client = self.client_address[0]


        cached = get(cache_key)
        if cached:
            status, headers, body = cached
            headers["X-Cache"] = "HIT"
            log_request(client, cache_key, "HIT")
            self._send_response(status, headers, body)
            return
        
        try:
            status, headers, body = forward_request(self.origin_url, self.path)
        except Exception as e:
            self.send_error(502, f"Bad Gateway: {e}")
            return
        
        headers = sanitize_headers(headers)
        headers["X-Cache"] = "MISS"
        log_request(client, cache_key, "MISS")

        if 200<= status < 400:
            set(cache_key, (status, headers.copy(), body))

        self._send_response(status, headers, body)

    def _send_response(self, status: int, headers: dict, body: bytes):
        if isinstance(body, str):
            body = body.encode("utf-8")
            
        self.send_response(status)
        for key, val in headers.items():
            if key.lower() not in ("content-length", "server", "date"):
                self.send_header(key, val)
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

def run_proxy(port: int, origin_url: str):
    def handler_factory(*args, **kwargs):
        return CachingProxyHandler(*args, origin_url=origin_url, **kwargs)
    
    server = http.server.HTTPServer(('localhost', port), handler_factory)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()