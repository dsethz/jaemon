import argparse
import logging
import sys
from typing import Any, Dict
import yaml

from jaemon.fetcher import fetch
from jaemon.parser import parse
from jaemon.store import JobStore
from jaemon.notifier import notify

logger = logging.getLogger(__name__)

def setup_logging() -> None:
    """Configure global logging format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    """Load and parse YAML configuration file."""
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as exc:
        logger.error("Failed to load config: %s", exc)
        sys.exit(1)

def run_scan() -> None:
    """Execute one scan cycle: fetch, parse, diff, notify."""
    config = load_config()
    store = JobStore("data/seen_jobs.db")
    new_jobs = []

    for url in config.get("searches", []):
        try:
            html = fetch(url)
            jobs = parse(url, html)
        except Exception:
            logger.exception("Error fetching/parsing URL: %s", url)
            continue

        for job in jobs:
            if store.is_new(job.id):
                new_jobs.append(job)
            store.mark_seen(job.id)

    store.cleanup(days=5)

    if new_jobs:
        try:
            notify(new_jobs, config.get("email", {}))
        except Exception:
            logger.exception("Failed to send notification email")
    else:
        logger.info("No new jobs found today.")

def add_url(url: str, path: str = "config.yaml") -> None:
    """Add a new search URL to config."""
    cfg = load_config(path)
    urls = cfg.setdefault("searches", [])
    if url in urls:
        logger.warning("URL already exists: %s", url)
        return
    urls.append(url)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f)
    logger.info("Added URL: %s", url)

def remove_url(url: str, path: str = "config.yaml") -> None:
    """Remove a search URL from config."""
    cfg = load_config(path)
    urls = cfg.get("searches", [])
    if url not in urls:
        logger.warning("URL not found: %s", url)
        return
    urls.remove(url)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(cfg, f)
    logger.info("Removed URL: %s", url)

def list_urls(path: str = "config.yaml") -> None:
    """List all configured search URLs."""
    cfg = load_config(path)
    logger.info("Tracked Search URLs:")
    for u in cfg.get("searches", []):
        print(f"- {u}")

def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(description="jaemon CLI")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("run", help="Perform one scan now")
    sub.add_parser("list-urls", help="List all tracked search URLs")
    a = sub.add_parser("add-url", help="Add a search URL")
    a.add_argument("url", help="Search URL with filters")
    r = sub.add_parser("remove-url", help="Remove a search URL")
    r.add_argument("url", help="URL to remove")

    args = parser.parse_args()
    if args.cmd == "run":
        run_scan()
    elif args.cmd == "list-urls":
        list_urls()
    elif args.cmd == "add-url":
        add_url(args.url)
    elif args.cmd == "remove-url":
        remove_url(args.url)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
