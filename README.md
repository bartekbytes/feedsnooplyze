# snooplyze

## Motivation & Main idea

I am often informed by other people (via LinkedIn Wall, etc...) about new functionalities (or changes in them) in tools I use.

So:

- I don't want to be behind with the newest updates.
- I want to be informed ASAP as the information is released by authors of these tools.

The idea is to create a software that will go through all relevant websites and checks if there is a new content.
If yes, inform me immediately.

## Main things to consider

### 1. Various tools and their info sources (Identify Information Sources)

- Official blogs / websites
- RSS feeds (many tools have them)
- GitHub release pages
- Twitter / X accounts
- LinkedIn pages
- Newsletters
- Reddit, StackOverflow, Discord, etc.

| Tool    | Info Source Type | URL                                 |
| :------ | :--------------- | :---------------------------------- |
| GitHub  | RSS feed         | https://github.blog/feed/           |
| VS Code | GitHub releases  | https://github.com/microsoft/vscode |
| Figma   | Blog             | https://www.figma.com/blog/         |
| Slack   | Changelog page   | https://slack.com/intl/en-changelog |

### Step 2: Choose the Notification Method

How do you want to be alerted?

- Email?
- Telegram message?
- Discord bot?
- Slack message?
- Desktop notification?
- Daily/weekly digest?

### Step 3: Implementation Plan

Depending on sources, we can use:

- feedparser for RSS
- requests + BeautifulSoup or Selenium for websites
- GitHub API for repo releases
- Twitter/X API for social media (requires setup)
- Scheduling via cron, APScheduler, or GitHub Actions

Output format:

- Simple script (Python is common)
- Web app (Flask/Django/Node.js)
- Mobile app (if you want push notifications)

## Requirements

### Functional Requirements:

### Non-functional Requirements:

## Tech Stack

- **Backend:** Python
- **Frontend:** _(TBD)_
- **Persistence:** _(TBD)_

## Details

## More Detailed Details

## Main points

## Example how to use classess directly

```python
def fetch():

    # Persistence Configuration, here Ducn DB engine
    ddbpe = DuckDbPersistenceEngine(database="../persistence/viz.duckdb")
    ddbpe.connect()

    # Creating both Pages and PageMonitors

    # 1. Create a fetch for Duck DB blog
    duckdb_page = Page(name = "Duck DB", url = "https://duckdb.org/news/")
    duckdb_monitor = PageMonitor(page = duckdb_page, parser = DivClassParser(div_class_name = "newstiles"), persistence = ddbpe, timeout = 10)

    # 2. Create a fetch for Databricks blog
    databricks_page = Page(name = "Databricks Blog", url = "https://www.databricks.com/blog")
    databricks_monitor = PageMonitor(page = databricks_page, parser=AllDocumentParser(), persistence = ddbpe, timeout = 10)

    # Poll every 60 seconds
    while True:
        time.sleep(60)
        monitors = [duckdb_monitor, databricks_monitor]
        [m.check_for_update() for m in monitors]

```
