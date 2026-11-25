# Social Listener: learning and operations guide

This guide describes the repository's current implementation. The technical, analysis, and digest design documents describe proposed capabilities, not a deployed service.

## Learning outcomes

- **API integration:** Keep external API behavior distinct from library method signatures; a client initializing successfully does not guarantee requests will work. Log and check failures rather than treating an empty result as success.
- **Database design:** Choose stable IDs for deduplication, separate collected records from analysis results, parameterize SQL, and understand the tradeoffs of denormalized fields and a processed flag.
- **Configuration and privacy:** Load credentials from environment variables, keep secrets out of source control, and account for working-directory-relative paths and local data retention.
- **Reliability and testing:** Validate third-party responses, preserve failed work for retry, update related state atomically, and test with temporary databases before running against persistent data.

## Architecture overview

| Component | Location | Current responsibility |
| --- | --- | --- |
| Configuration | `src/config.py` | Loads `.env` and reads API credentials, database path, and default subreddits. |
| Entry point | `src/main.py` | Initializes components, attempts collection, and processes up to three pending posts in one run. |
| Reddit collector | `src/collectors/reddit_collector.py` | Uses PRAW for post listings, searches, and a standalone comment helper. The entry point calls only the listing method, which currently fails as described below. |
| X collector | `src/collectors/x_collector.py` | A stub that logs warnings and returns empty lists; the entry point does not call it. |
| Analyzer | `src/analyzers/claude_analyzer.py` | Sends post title and content to Claude for sentiment, topics, and a summary. Its hard-coded model has been retired. |
| Database | `src/database/db_manager.py` | Creates SQLite tables and exposes post and analysis operations. |

The intended flow is:

1. `main.py` loads configuration and creates the SQLite database if needed.
2. It attempts to fetch up to five hot posts from each of the first two configured subreddits, `programming` and `webdev`. The current PRAW argument mismatch prevents these calls from collecting posts.
3. Collected posts would be inserted with platform-prefixed IDs. Existing IDs are ignored rather than refreshed.
4. Up to three rows with `processed = 0` are selected, with no guaranteed ordering. For each, the analyzer makes three separate Claude SDK calls: one each for sentiment, topics, and summary.
5. The entry point attempts to save the combined result and then marks the post processed. These are separate database operations; failures and fallback results do not reliably stop the processed flag from being set.

There is no web server, scheduler, digest delivery, or automatic comment storage in this flow. The application exits after one run.

## API integration lessons

### Reddit and PRAW

- PRAW wraps Reddit's API and uses the client ID, client secret, and user agent from configuration. Creating a client does not prove that the credentials or network access work; a request is needed to verify them. Provider access and rate limits are subject to Reddit's current policies.
- The collector converts PRAW objects into dictionaries before storing them. Post IDs are prefixed with `reddit_`, deleted authors become `[deleted]`, and stickied posts are skipped by the listing method after fetching.
- `search_posts` is separate from the broken hot-post path and searches a specified subreddit, or all subreddits if none is supplied. The comment helper takes a Reddit submission ID and returns comment dictionaries, but the entry point neither calls it nor saves comments.
- Match parameters to the specific API method. The pinned PRAW 7.7.0 `hot()` listing does not accept `time_filter`; passing it reaches `ListingGenerator` and raises an error. PRAW's `search()` does accept that argument. The collector logs errors and returns an empty or partial list, so an empty result is not proof of a successful request.
- There is no application-level retry or backoff policy around collection. Respect provider limits and inspect the logs rather than assuming an empty list means no posts matched.

See the [PRAW 7.7.0 listing methods](https://github.com/praw-dev/praw/blob/v7.7.0/praw/models/listing/mixins/base.py), [listing generator](https://github.com/praw-dev/praw/blob/v7.7.0/praw/models/listing/generator.py), and [subreddit search](https://github.com/praw-dev/praw/blob/v7.7.0/praw/models/reddit/subreddit.py) for the argument behavior.

### Claude

- `analyze_full` concatenates a post's title and content and makes three separate SDK calls. This sends that text to Anthropic and can incur usage charges; use small samples and do not send content you are not permitted to share.
- Each prompt asks for JSON. The code parses the response with `json.loads`, but does not validate its schema or guarantee that the model's judgments are correct. Review results rather than treating sentiment or summaries as facts.
- The hard-coded model is `claude-3-5-sonnet-20241022`. Anthropic [retired it on October 28, 2025](https://platform.claude.com/docs/en/about-claude/model-deprecations), so the current Anthropic API calls require a code change to use an available model. There is no environment variable for selecting the model.
- API, parsing, and other exceptions are logged and replaced with `unknown` sentiment, empty topics, or `Unable to summarize`. The entry point may save those fallbacks and mark the post processed. SDK-level retries can also make more network attempts than the three top-level calls.

## Database design decisions

SQLite provides a local, single-file database without a separate server. `DatabaseManager` creates its parent directory and tables on initialization.

| Table | Contents and role |
| --- | --- |
| `posts` | Text primary key, source/platform, post metadata, timestamps, and a `processed` flag used to find pending work. |
| `comments` | Comment fields and a declared reference to `posts`; there is currently no database method or pipeline step to insert comments. |
| `analysis_results` | Auto-incrementing ID, a declared post reference, analysis type, sentiment, comma-separated topics, summary, and raw analysis. Multiple rows can refer to one post. |

The post ID allows `INSERT OR IGNORE` to avoid duplicate rows on repeated collection. It does not update existing scores or text, and `insert_post` can return `True` even when no row was inserted. Queries use SQL parameters instead of interpolating values.

Important prototype tradeoffs:

- The schema declares foreign keys, but connections do not enable `PRAGMA foreign_keys = ON`; SQLite normally leaves enforcement off per connection.
- Saving an analysis and marking a post processed use separate connections and transactions. The entry point does not check their return values, so a failed insert or fallback analysis can still leave a post marked processed.
- Topics are stored as a comma-separated string, and `raw_analysis` is Python's string representation of a dictionary, not guaranteed JSON. There is no migration system or retry queue.
- Reddit creation times are converted to naive local timestamps, while SQLite's default `collected_at` and analysis `created_at` timestamps use UTC. Compare them carefully.
- The database can contain authors, post text, and analysis. Keep the `.db` file and backups private; `.gitignore` excludes database files but does not protect copies stored elsewhere.

## Local deployment guide

The supported deployment described here is a local, manually started process. There is no container, cloud deployment configuration, or scheduler in this repository. The draft technical design discusses a possible hosted architecture, not steps that can be run today.

From the repository root, create a virtual environment using Python 3.9 or later with SQLite available:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS or Linux, activate it with `source venv/bin/activate` instead. Install the dependencies used by the current application:

```text
python -m pip install "praw==7.7.0" "anthropic==0.28.0" "python-dotenv==1.0.0" "httpx==0.27.2"
```

This is a temporary workaround: `requirements.txt` incorrectly lists the standard-library module `sqlite3` as a pip package, and the pinned Anthropic SDK is incompatible with HTTPX 0.28 or later.

Copy `.env.example` to `.env` (`Copy-Item .env.example .env` on Windows, or `cp .env.example .env` on macOS/Linux). Add `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, and a descriptive `REDDIT_USER_AGENT` for collection. Set `ANTHROPIC_API_KEY` before attempting analysis. The existing environment takes precedence over `.env`; do not commit or share credentials. X credentials are unused by the current entry point.

Leave `DB_PATH=./data/social_listener.db` for the default location, or set it to an absolute path for a consistent location across working directories. Relative paths resolve against the directory from which Python is started, not the location of `.env`.

Use the search example below to try collection independently. The default entry point cannot collect hot posts as shipped, and its retired model cannot produce successful Anthropic analysis. Once those issues are fixed separately, run `python .\src\main.py` on Windows or `python src/main.py` on macOS/Linux from the repository root. Until then, running it can log collection errors and mark existing pending posts processed with fallback analysis. Back up any existing database before experimenting.

### Try Reddit search

With the virtual environment active and Reddit credentials configured, start `python` from the repository root and enter:

```python
import sys
sys.path.insert(0, "src")

from config import get_config
from collectors.reddit_collector import RedditCollector
from database.db_manager import DatabaseManager

config = get_config()
collector = RedditCollector(
    config.REDDIT_CLIENT_ID, config.REDDIT_CLIENT_SECRET, config.REDDIT_USER_AGENT
)
db = DatabaseManager(config.DB_PATH)
posts = collector.search_posts("python", subreddit="python", limit=5)
print(f"Returned {len(posts)} posts")
for post in posts:
    if not db.insert_post(post):
        print(f"Could not store {post['id']}; check the logs")
```

This uses Reddit but does not call Claude. Check logs if the result is empty; duplicates may already exist in the database. Exit the Python shell when finished.

### Inspect the database

From the repository root, start `python` and use the following for the default `DB_PATH`. If you configured another path, use that path instead. The existence check avoids accidentally creating an empty database during inspection.

```python
import sqlite3
from pathlib import Path

path = Path("data") / "social_listener.db"
if not path.is_file():
    raise FileNotFoundError(path)

connection = sqlite3.connect(path)
for row in connection.execute(
    "SELECT p.id, p.processed, a.sentiment, a.summary "
    "FROM posts AS p LEFT JOIN analysis_results AS a ON p.id = a.post_id "
    "LIMIT 10"
):
    print(row)
connection.close()
```

An unprocessed post has `processed = 0`. A processed flag or an analysis row alone does not establish that the Claude calls succeeded; inspect the logs and results. For a local backup, stop the application first and copy the configured database file to a private location. Preserve it when moving the application: without persistent storage, the next run starts with a new database.

## Troubleshooting

| Symptom | Cause and next step |
| --- | --- |
| `pip install -r requirements.txt` cannot find `sqlite3==3.44.0` | `sqlite3` is part of Python's standard library, not the pip dependency listed in the file. Use the minimal install command above and ensure your Python installation includes SQLite. |
| `Client.__init__()` reports an unexpected `proxies` argument | Anthropic SDK 0.28.0 passes `proxies` to HTTPX, which removed it in 0.28. Use `httpx==0.27.2` in this virtual environment. See the [SDK source](https://github.com/anthropics/anthropic-sdk-python/blob/v0.28.0/src/anthropic/_base_client.py) and [HTTPX changelog](https://github.com/encode/httpx/blob/0.28.0/CHANGELOG.md). |
| `ModuleNotFoundError` | Activate the intended virtual environment and use `python -m pip` with the same Python executable used to run the application. |
| Reddit collection logs an unexpected `time_filter` argument | The default hot-post call is incompatible with PRAW 7.7.0. Use the independent search example above or fix the listing method in a separate code change; changing from hot to top would also change the ranking behavior. |
| Reddit search returns no posts | Check the collector's error logs, credentials, user agent, network access, and Reddit's access/rate limits. An empty list can represent an error or no matches. |
| Claude logs model-not-found errors, or results contain `unknown`/empty fallback values | The configured model is retired. A supported model must be selected in code; also check credentials, network access, provider limits, response parsing, and usage. The current pipeline can mark failed analyses processed. |
| The database appears empty or is in an unexpected place | Run from the repository root, check `DB_PATH` and its working-directory-relative resolution, and inspect collection errors. Repeated post IDs are ignored rather than updated. |
| Changing `LOG_LEVEL` has no effect | The configuration reads this variable, but `main.py` configures logging at `INFO` directly. |
| X results, comments, a dashboard, or a digest are missing | X is a stub; comments are not stored by the pipeline; dashboard and digest functionality are planned, not implemented. |

There is no built-in requeue command for failed analyses. Back up the database before any manual edits; reprocessing can create additional analysis rows and incur further API charges.

The existing database tests use Python's standard library and do not call external APIs: `python -m unittest discover -s tests -v`.

## Future enhancements

- Fix the PRAW hot-listing call and select an available Claude model through configuration; correct and lock compatible dependencies.
- Add explicit failure states, retries, atomic analysis/processed updates, and tests for API and database failure paths.
- Enable and test foreign-key enforcement, add schema migrations, and store structured analysis in a defined format.
- Implement X collection, comment persistence, scheduling, a digest, and a dashboard if those features remain desired.
- Add rate-limit and cost monitoring, retention controls, and an intentional hosted deployment with persistent storage and secure secrets.