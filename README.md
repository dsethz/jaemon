````markdown
# jaemon

A lightweight Python CLI and background service that scans specified job search URLs daily and notifies you via email when new postings appear — installable via `pip install .`.

## Features

- **Daily scanning** of configured job board URLs
- **Deduplication**: tracks seen job IDs in SQLite
- **Email notifications** with summary of new postings
- **Configurable** via `config.yaml` (search URLs + SMTP credentials)
- **Logging** for monitoring and debugging
- **Testing & CI**: pytest, ruff, black, isort, pre-commit, GitHub Actions
- **Pip-installable** as a standard Python package

## Installation

```bash
git clone https://github.com/yourusername/jaemon.git
cd jaemon
# install locally
pip install .
# or in editable/dev mode:
pip install -e .[dev]
````

## Configuration

1. Copy `config.yaml.example` to `config.yaml`.
2. Edit `config.yaml`:

   ```yaml
   searches:
     - https://www.indeed.com/jobs?q=python+remote&l=Zurich
   email:
     smtp_server: smtp.example.com
     smtp_port: 587
     username: you@example.com
     password: supersecret
     from_addr: you@example.com
     to_addr: you@personal.com
   ```

## Usage

Run commands via the `jaemon` entry point:

```bash
# perform one scan immediately
jaemon run

# add/remove/list search URLs
jaemon add-url "https://..."
jaemon remove-url "https://..."
jaemon list-urls
```

## Scheduling

Start the built‑in scheduler:

```bash
jaemon scheduler
```

By default it runs daily at 08:00 Europe/Zurich. You can also use your OS’s scheduler (cron, launchd, Task Scheduler) to call `jaemon run`.

## Project Structure

```text
jaemon/
├── .gitignore               # ignore secrets, env, bytecode
├── jaemon/                  # Python package
│   ├── __init__.py
│   ├── cli.py               # CLI entry point
│   ├── scheduler.py         # scheduling logic
│   ├── fetcher.py           # HTTP fetching
│   ├── parser.py            # HTML parsing
│   ├── store.py             # SQLite store
│   ├── notifier.py          # email notifications
│   └── config.yaml.example  # example configuration (without secrets)
├── tests/                   # pytest tests
├── .github/workflows/ci.yml # CI pipeline
├── pyproject.toml           # packaging & dependencies
├── .pre-commit-config.yaml  # pre-commit hooks
├── .ruff.toml               # ruff configuration
└── README.md                # this file
```

```
```

