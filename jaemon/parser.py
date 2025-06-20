import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from dataclasses import dataclass
from typing import Callable, Dict, List

logger = logging.getLogger(__name__)

@dataclass
class Job:
    """Represents a job posting."""
    id: str
    title: str
    link: str
    date: str

PARSERS: Dict[str, Callable[[str], List[Job]]] = {}


def default_parser(html: str) -> List[Job]:
    """Generic HTML parser for job listings."""
    soup = BeautifulSoup(html, "html.parser")
    jobs: List[Job] = []
    for card in soup.select(".job-card"):
        try:
            job_id = card.get("data-id") or card.a["href"]
            title = card.select_one("h2").get_text(strip=True)
            link = card.a["href"]
            date = card.select_one(".date").get_text(strip=True)
            jobs.append(Job(id=job_id, title=title, link=link, date=date))
        except Exception:
            logger.exception("Error parsing job card")
            continue
    return jobs


def parse(url: str, html: str) -> List[Job]:
    """Select site-specific parser or fallback."""
    domain = urlparse(url).netloc.replace("www.", "")
    parser_fn = PARSERS.get(domain, default_parser)
    return parser_fn(html)
