import argparse
import sys
from pathlib import Path
from .cache import load_cache, clear_cache, CACHE_FILE
from .proxy import run_proxy

def parse_args():
    parser = argparse.ArgumentParser(description="Simple caching proxy server (GET-only)")
    parser.add_argument("--port", type=int, help="Port to run the proxy")
    parser.add_argument("--origin", type=str, help="Origin server URL (e.g., http://dummyjson.com)")
    parser.add_argument("--clear-cache", action="store_true", help="Clear the local cache and exit")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.clear_cache:
        clear_cache()
        print("cache cleared ... ")
        return
    
    if not args.port or not args.origin:
        print("Error: --port and --origin are required unless usin --clear-cache", file=sys.strderr)
        parse_args().print_help()
        sys.exit(1)

    if not args.origin.startswith(("http://", "https://")):
        print("Origin must start with http:// or https://", file=sys.stderr)
        sys.exit(1)
    
    load_cache()
    print(f"Starting caching proxy on http://localhost:{args.port}")
    print(f"Forwarding to origin: {args.origin}")
    print(f"Cache file: {CACHE_FILE.absolute()}")
    print("Press Ctrl+C to stop.\n")

    try:
        run_proxy(args.port, args.origin)
    except KeyboardInterrupt:
        print("\n Shutting down gracefully ...")