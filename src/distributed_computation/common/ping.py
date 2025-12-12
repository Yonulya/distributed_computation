import subprocess
import platform


def ping_host(host: str) -> tuple[str, bool]:
    """
    Ping a host once.
    Returns (host, success)
    """
    system = platform.system().lower()

    if system == "windows":
        cmd = ["ping", "-n", "1", host]
    else:
        cmd = ["ping", "-c", "1", host]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3,
        )
        return host, result.returncode == 0
    except Exception:
        return host, False
