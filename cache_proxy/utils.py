import sys

def sanitize_headers(headers: dict) -> dict:
    """Remove hop-by-hop headers per RFC 7230."""
    hop_by_hop = {"connection", "transfer-encoding", "keep-alive", "proxy-connection", "upgrade"}
    return {k: v for k, v in headers.items() if k.lower() not in hop_by_hop}

def log_request(client_addr: str, path: str, cache_status: str = "MISS"):
    print(f"[{client_addr}] {cache_status} -> {path}", file=sys.stderr)