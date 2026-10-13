"""tests/unit/utils/test_url.py"""

from __future__ import annotations

import pytest

from octop.infra.utils.url import canonical_browser_url, normalize_nav_url


def test_empty_and_blank() -> None:
    assert normalize_nav_url("") == ""
    assert normalize_nav_url("   ") == ""


def test_bare_host_is_prefixed() -> None:
    assert normalize_nav_url("baidu.com") == "https://baidu.com"
    assert normalize_nav_url("example.com/a?q=1") == "https://example.com/a?q=1"


def test_absolute_http_urls_are_preserved() -> None:
    assert normalize_nav_url("http://x.com/") == "http://x.com/"
    assert normalize_nav_url("https://x.com/") == "https://x.com/"
    assert normalize_nav_url("HTTPS://x.com/") == "HTTPS://x.com/"


def test_protocol_relative_url_gets_https() -> None:
    """`//host` is a relative scheme URL (common when copied from a page source);
    it must not become the hostless https:////host."""
    assert normalize_nav_url("//baidu.com") == "https://baidu.com"
    assert normalize_nav_url("//example.com/path?q=1") == "https://example.com/path?q=1"


def test_non_http_scheme_with_slashes_is_rejected() -> None:
    assert normalize_nav_url("ftp://x.com") == ""


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/search_result?q=1",
        "https://www.xiaohongshu.com.evil.test/search_result?q=1",
        "https://www.xiaohongshu.com/search_result/?q=1",
        "https://www.xiaohongshu.com/explore?q=1",
        "http://www.xiaohongshu.com/search_result?q=1",
    ],
)
def test_browser_url_keeps_other_hosts_paths_and_schemes(url: str) -> None:
    assert canonical_browser_url(url) == url
