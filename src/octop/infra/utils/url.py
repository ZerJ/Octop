"""URL helpers shared across infra and API layers."""

from urllib.parse import urlsplit, urlunsplit


def canonical_browser_url(url: str) -> str:
    """Avoid Xiaohongshu's search redirect from HTTPS to HTTP.

    The slashless search endpoint redirects to HTTP and can stall Chrome's
    page CDP connection. Its HTTPS endpoint with a trailing slash loads directly.
    """
    parts = urlsplit(url)
    if (
        parts.scheme.lower() == "https"
        and parts.hostname in {"www.xiaohongshu.com", "xiaohongshu.com"}
        and parts.path == "/search_result"
    ):
        return urlunsplit(parts._replace(path="/search_result/"))
    return url


def normalize_nav_url(raw: str) -> str:
    """``baidu.com`` → ``https://baidu.com``; empty input → ``\"\"``."""
    t = raw.strip()
    if not t:
        return ""
    lower = t.lower()
    if "://" in lower:
        if lower.startswith(("http://", "https://")):
            return t
        return ""
    if t.startswith("//"):
        # Protocol-relative URL (e.g. pasted from a page source): keep the host
        # and force https, instead of producing "https:////host" with an empty
        # host name.
        return f"https://{t[2:]}"
    return f"https://{t}"
