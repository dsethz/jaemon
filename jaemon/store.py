import logging
import os
import sqlite3
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class JobStore:
    """SQLite-backed store for seen jobs with cleanup."""
    def __init__(self, path: str = "data/seen_jobs.db") -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS seen(id TEXT PRIMARY KEY, last_seen TIMESTAMP)"
        )

    def is_new(self, job_id: str) -> bool:
        """Check if a job ID has not been seen."""
        cur = self.conn.execute(
            "SELECT 1 FROM seen WHERE id = ?", (job_id,)
        )
        is_new_job = cur.fetchone() is None
        logger.debug("Job %s is new: %s", job_id, is_new_job)
        return is_new_job

    def mark_seen(self, job_id: str) -> None:
        """Mark a job ID as seen with current timestamp."""
        now = datetime.utcnow().isoformat()
        self.conn.execute(
            "INSERT INTO seen(id, last_seen) VALUES (?, ?)"
            " ON CONFLICT(id) DO UPDATE SET last_seen=excluded.last_seen",
            (job_id, now),
        )
        self.conn.commit()
        logger.debug("Marked job %s as seen", job_id)

    def cleanup(self, days: int = 5) -> None:
        """Remove entries older than specified days."""
        threshold = (datetime.utcnow() - timedelta(days=days)).isoformat()
        self.conn.execute(
            "DELETE FROM seen WHERE last_seen < ?", (threshold,)
        )
        self.conn.commit()
        logger.info("Cleaned up entries older than %d days", days)
