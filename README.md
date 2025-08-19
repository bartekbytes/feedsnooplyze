# Snooplyze

## 🚧 Work in Progress

`This project is currently under active development. Please note that some compromises have been made regarding code quality, structure, and best practices to prioritize progress and experimentation. Improvements and refactoring are planned as the project evolves.`

## 📚 General Details and Deep Dive Technical Details

❗ This file (`README.md`) consists of a general overview of the project, without
going into too deep technical details. More technical details can be found in `docs\technical-overview.md` file.

## 🎯 Motivation & Main Idea

I often learn about new technologies, features, or tool updates from others—usually via _LinkedIn feeds_, _Medium posts_, and similar sources.

So I asked myself:

- How can I **avoid falling behind** on important updates?
- How can I **get notified the moment something is published** — directly from the source?

That’s why I built **Snooplyze**:
A tool that regularly scans selected information sources and alerts me immediately when new content appears.

## 🗺️ 10,000-Foot Overview

Here’s a high-level look at how **Snooplyze** works. (For a detailed breakdown, see the full documentation.)

- Relevant websites to monitor are defined in a configuration file.
- The application runs — either manually or on a schedule.
- It fetches and compares the current content with what’s stored:
  - **No changes** → nothing happens.
  - **New content** → it’s extracted, users are notified, and the update is saved in persistent storage.

## ⚙️ Main Functionalities

Core features and capabilities (non-technical overview):

- Configure the application via an external config file
- Define content sources (**Pages**) through a separate configuration file
- Set up how content is extracted (**parsing** rules)
- Store content and track changes using a **Persistence Layer**
- Send **Notifications** to users in various formats

## 🧰 Tech Stack

- ⚙️ **Backend**: Python 3.12 🐍
- 💻 **Frontend**: TBD – Not yet started. Potential options include **Streamlit**, **Reflex**, or more advanced frameworks like **React**.
- 💾 **Persistence**: Supports **SQLite**, **DuckDB**, **PostgreSQL**, and **MySQL** (with more planned).

# 🧩 Components

Below is a brief overview of the key components:

- 📰 **Pages** – Define the websites to monitor
- 🧬 **Parsers** – Extract relevant content from **Pages**
- 📢 **Notifications** – Alert users when new content is detected
- 💾 **Persistence Layer** – Stores and tracks previously fetched content

## 📰 Pages (Content Sources)

### Content sources

There are exist many sources of information, like:

- Blogs and websites
- RSS feeds (common for many tools)
- GitHub release pages
- Twitter / X accounts
- LinkedIn pages
- Newsletters
- Communities like Reddit, StackOverflow, Discord, and more

### Pages

Currently, only Blogs and Websites are supported; other sources will be added later.

Pages are defined in the _Page Configuration File_, where each entry is called a **Page** with these attributes:

- **Name**: Unique, descriptive identifier (e.g., `DuckDB Blog`, `MS Azure Newsletter`)
- **URL**: Full link to the page (e.g., "https://duckdb.org/news/")
- **Description**: A brief note to help identify the page
- **Parser**: Specifies which parser to use for extracting content (see _Parsers_ section)

Example:

```yaml
Pages:
  - name: "Duck DB"
    url: "https://duckdb.org/news/"
    description: "Duck DB News Page"
    parser:
      - type: "div_class"
        class_name: "newstiles"
```

## 🧬 Parsers

**Parsers** handle content extraction by processing a **Page** and pulling out relevant data based on their configuration.

There are two types of Parsers:

- **Generic Parsers**: Can be used with any Page but require configuration for each one.
- **Custom Parsers**: Designed specifically for certain **Pages** (e.g., DuckDBBlogParser for DuckDB Blog). These come pre-configured and don’t require setup.

## 📢 Notifications

### Notification methods

Various types of notification methods that can be considered:

- Console
- Flat File
- Email
- Telegram message
- Discord bot
- Slack message
- Desktop notification
- Daily/weekly digest

Currently, only **Console**, **Flat File**, and **Email** are implemented. More will be added in the future.

### Notifications

**Notifications** are configured via the **NotificationConfig** section in the _Application Configuration File_.

Example:

```yaml
NotificationConfig:
  - notification_type: console
```

## 💾 Persistence Layer

The **Persistence Layer** stores information about **Pages** and their Content, enabling the application to track changes over time. It also supports storing data necessary for sending **notifications**.

This layer is configured via the **PersistenceConfig** section in the _Application Configuration File_. Currently, it supports multiple database engines (e.g., SQLite, DuckDB, PostgreSQL, MySQL), with more planned.

# ▶️ How to run

## ⚙️ Configure Snooplyze

Snooplyze requires two configuration files:

- **Application Configuration File**
  - Always named `config.yaml`
  - Valid YAML format
  - Defines three sections:
    - `GeneralConfig` — general app settings
    - `PersistenceConfig` — persistence layer settings
    - `NotificationConfig` — notification settings
- **Pages Configuration File**
  - Can have any filename
  - Valid YAML format
  - Defines the Pages to monitor and their content parsing setup

Example files are provided in the project root:

- `config.yaml.example` (Application Configuration)
- `snooplyze.yaml.example` (Pages Configuration)

❗ For detailed setup instructions, see `docs/technical-overview.md`.

## 🏃‍♂️ Run Snooplyze

You can run Snooplyze in two ways:

Directly

- (Optional) Create and activate a Python virtual environment
- Install dependencies from `requirements.txt`
- Run:
  - Run as a module (from the root folder) `python -m snooplyze <your_arguments>` with the required arguments (see below) or
  - After installing application as a Python package (`pip install -e .`): `snooplyze <your_arguments>` with the required arguments (see below)

Via Docker

- Use the provided `Dockerfile` to build an image
- Run the container standalone or with other services using `docker-compose.yaml`

## 🔧 Arguments

Below is a list of all **command-line arguments** supported by the application:

- `-r` / `--run-mode`: setup (init persistence) or fetch (fetch page content).
- `-ft` / `--fetch-type`: Used with fetch. interactive (loop) or oneshot (run once).
- `-p` / `--pooling-time`: Optional. Interval in seconds for interactive mode.
- `-f` / `--config-file`: Required in fetch mode. Path to the Pages Configuration File.

# 📅 Roadmap

✅ - Done | 🚧 - Work in Progress | ⏳ - Planned, not started

## Basics

- ✅ Basic configuration via Config File
- ✅ Configuration of Pages via Config File
- 🚧 Advanced validation of Config Files
- 🚧 Increase test coverage, writing more tests (❗ important)
- 🚧 Refactoring code to introduce `registry pattern` instead of spaghetti-like `if-elif-elif-...-elif-else`

# Advanced Features

- ⏳ Weekly / Monthly summary of changes (as a report, etc...)
- ⏳ Some analytics
- ⏳ GUI
- ⏳ Extraction of Content change and perform a summarization of the Content (_NLP_)

## Persistence Layer

- ✅ Basic Persistence Layer logic
- ✅ Adding first Persistence Engines
- 🚧 Refactoring the layer to use OOM, like SQL Alchemy (❗ important)
- ⏳ Adding more Persistence Engines

## Pages

- ✅ Basic Page configuration via Config File
- 🚧 Validation of Pages (Unique name of Page)
- ⏳ Adding more Attributes to Pages (and Config File), like Tags

## Parsers

- ✅ Basic Parser configuration via Config File
- ✅ Basic parsing logic
- Separation to **Generic** Parsers and **Custom** Parsers
- Add more **Custom Parsers**
- Enable ability to write **Custom Parsers** via external config file (as plug-in), not in the code
- Async and multithreading parsing (to enable parsing multiple Pages simultaniousely)

## Notifications

- ✅ Configuration mechanism
- ✅ Notificatgion executon logic
- ✅ Console Notification
- ✅ Flat File Notification
- ✅ Email Notification
  - ✅ Email Template
- ✅ Telegram Notification
- ⏳ Slack Notification
- ⏳ Discord Notification
- ⏳ WhatsApp Notification
- ⏳ Teams Notification
