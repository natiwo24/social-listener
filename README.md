# Social Listener

Social Listener is a learning project for collecting developer conversations from Reddit, storing them in SQLite, and analyzing post text with the Claude API.

## Current status

This repository contains a single-run Python prototype, not a deployed service. Reddit search and SQLite storage are implemented; X/Twitter collection, scheduling, dashboards, and email digests are not.

**The default pipeline currently has two blockers:** the Reddit hot-post call is incompatible with the pinned PRAW version, and the hard-coded Claude model has been retired. The program can still mark posts as processed after analysis fails. Read the [learning and operations guide](docs/LEARNING_GUIDE.md) before running it on data you want to keep.

## Local setup

Use Python 3.9 or later, with SQLite available in the Python installation. From the repository root, create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS or Linux, activate it with `source venv/bin/activate` instead.

Install the dependencies used by the current application:

```text
python -m pip install "praw==7.7.0" "anthropic==0.28.0" "python-dotenv==1.0.0" "httpx==0.27.2"
```

This is a temporary workaround: `requirements.txt` incorrectly lists the standard-library module `sqlite3` as a pip package, and the pinned Anthropic SDK is incompatible with HTTPX 0.28 or later. See [troubleshooting](docs/LEARNING_GUIDE.md#troubleshooting) before installing.

Copy `.env.example` to `.env` (`Copy-Item .env.example .env` on Windows, or `cp .env.example .env` on macOS/Linux). Set `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and a descriptive `REDDIT_USER_AGENT` for Reddit. Set `ANTHROPIC_API_KEY` before attempting analysis. Keep `.env` private; the repository ignores it. The X credentials are unused by the current entry point.

The default database is `data/social_listener.db`, relative to the working directory. Running from a different directory changes that location unless `DB_PATH` is set to an absolute path.

The [guide](docs/LEARNING_GUIDE.md#try-reddit-search) shows how to collect and inspect posts using the existing search method without running the broken default pipeline.

After reviewing the limitations, run the current entry point from the repository root:

```powershell
python .\src\main.py
```

On macOS or Linux, use `python src/main.py`.

## Documentation

- [Learning and operations guide](docs/LEARNING_GUIDE.md): architecture, API integration, database design, local deployment, troubleshooting, and future work.
- [Technical design](docs/TECHNICAL_DESIGN.md), [analysis design](docs/ANALYSIS_DESIGN.md), and [digest design](docs/DIGEST_DESIGN.md): drafts describing proposed capabilities, not the current deployment.

## Tests

The existing database tests use Python's standard library and do not call external APIs:

```text
python -m unittest discover -s tests -v
```

## References

- [PRAW documentation](https://praw.readthedocs.io/)
- [Claude API documentation](https://platform.claude.com/docs/)
- [SQLite documentation](https://www.sqlite.org/docs.html)
