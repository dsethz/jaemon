from jaemon.parser import default_parser, Job


def test_default_parser_empty():
    assert default_parser("") == []


def test_default_parser_basic():
    html = '<div class="job-card" data-id="123"><h2>Test</h2><a href="/job/123"></a><span class="date">Today</span></div>'
    jobs = default_parser(html)
    assert isinstance(jobs[0], Job)
    assert jobs[0].id == '123'
