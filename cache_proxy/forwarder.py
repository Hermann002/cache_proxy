import http.client
import urllib.parse
from typing import Tuple, Dict, Optional

def forward_request(origin_url: str, path: str) -> Tuple[int, Dict[str, str], bytes]:
    """_summary_
    Forward a GET request to the origin server
    Returns:
        (status_code, headers, body)
    """

    parsed = urllib.parse.urlparse(origin_url)
    full_path = path

    conn = None
    try:
        if parsed.scheme == "https":
            conn = http.client.HTTPSConnection(parsed.netloc, timeout=10)
        else:
            conn = http.client.HTTPConnection(parsed.netloc, timeout=10)

        conn.request("GET", full_path, headers={"Host": parsed.netloc})
        resp = conn.getresponse()

        status = resp.status
        headers = dict(resp.getheaders())
        body = resp.read()

        return status, headers, body
    
    finally:
        if conn:
            conn.close()