import logging
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
from jaemon.cli import run_scan, setup_logging


def main() -> None:
    """Configure and start daily scheduler with misfire settings."""
    setup_logging()
    scheduler = BlockingScheduler(timezone="Europe/Zurich")
    scheduler.add_job(
        run_scan,
        "cron",
        hour=8,
        minute=0,
        misfire_grace_time=10800,  # 3 hours grace time
        coalesce=True,
    )
    logging.info("[Scheduler] Starting daily job at 08:00 Europe/Zurich (misfire)")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped by user.")

if __name__ == "__main__":
    main()
