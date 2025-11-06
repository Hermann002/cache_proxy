import pickle
import threading
from pathlib import Path
import sys

CACHE_FILE = Path(".caching_proxy_cache.pkl")
_cache = {}
_cache_lock = threading.Lock()

def load_cache():
    global _cache
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "rb") as f:
                _cache.update(pickle.load(f))
        except Exception as e:
            print(f"Failed to load cache: {e}", file=sys.stderr)

def save_cache():
    try:
        with open(CACHE_FILE, "wb") as f:
            pickle.dump(_cache, f)
    except Exception as e:
        print(f"Failed to save cache: {e}", file=sys.stderr)

def clear_cache():
    global _cache
    with _cache_lock:
        _cache.clear()
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()

def get(key):
    with _cache_lock:
        return _cache.get(key)
    
def set(key, value):
    with _cache_lock:
        _cache[key] = value
    save_cache()

__all__ = ["get", "set", "load_cache", "clear_cache", "CACHE_FILE"]