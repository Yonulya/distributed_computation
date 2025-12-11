"""
Ping task executed by workers.
This module must be importable by the worker process. We keep it minimal and cross-platform:
- Use pythonping (pure Python) so it works on both Windows/Ubuntu without subprocess differences.
"""
from pythonping import ping

def ping_host(hostname: str, count: int = 1, timeout: int = 1):
    """Return (hostname, status).
    status could be 'up' or 'down' or an error string.
    """
    try:
        resp = ping(hostname, size=40, count=count, timeout=timeout)
        # If any packet received, consider host up
        ok = any([p.success for p in resp._responses])
        return hostname, "up" if ok else "down"
    except Exception as e:
        return hostname, f"error:{e}"