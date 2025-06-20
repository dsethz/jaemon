import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)
_session = requests.Session()
_retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
_session.mount("https://", HTTPAdapter(max_retries=_retries))
_session.mount("http://", HTTPAdapter(max_retries=_retries))


def fetch(url: str, timeout: int = 10) -> str:
    """Fetch URL content with retry logic."""
    try:
        response = _session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except Exception:
        logger.exception("Failed to fetch URL: %s", url)
        raise
