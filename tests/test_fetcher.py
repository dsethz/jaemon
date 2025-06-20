import pytest
from jaemon.fetcher import fetch

class DummyResponse:
    text = "<html></html>"
    def raise_for_status(self):
        pass

def test_fetch_success(monkeypatch):
    monkeypatch.setattr('jaemon.fetcher._session.get', lambda url, timeout: DummyResponse())
    assert fetch("http://example.com") == "<html></html>"
