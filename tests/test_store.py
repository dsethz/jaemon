import tempfile
from jaemon.store import JobStore


def test_store(tmp_path):
    db_path = tmp_path / "seen.db"
    store = JobStore(str(db_path))
    assert store.is_new("job1")
    store.mark_seen("job1")
    assert not store.is_new("job1")
    store.cleanup(days=0)
