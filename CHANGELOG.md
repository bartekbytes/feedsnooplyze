# Changelog

All notable changes to this project will be documented in this file.

## [0.1.19] - 2025-08-05

### Changes

- Make the codebase modular [#17]
- Add `pytest` testing engine and some first tests [#19]

## [0.1.18] - 2025-08-03

### Changes

- Add example files for both Configuration Files: [#16]
  - Application Configuration File - `config.yaml.example`
  - Pages Configuration File - `snooplyze.yaml.example`

## [0.1.17] - 2025-08-03

### Changes

- Add docstring for classess, enums, methods, ... [#15]

## [0.1.16] - 2025-08-03

### Changes

- **Telegram** Notification added [#14]
  - All the logic needed:
  - Configuration
  - Creation of Notification
  - Sending mechanism
  - Instructions (`technical-overview.md` updated; `telegram-setup.md` created)
- Enhancements for error capture when HTTP Request (`request`) is send.
- `gmail-setup.md` Instruction added (how to obtain App Password).

## [0.1.15] - 2025-08-03

### Changes

- Refactoring **Parser** mechanism by using a `registry pattern` (still need to handle a special case with parameters, though)

## [0.1.14] - 2025-08-02

### Changes

- `.dockerignore` file added
- `Dockerfile` file added

## [0.1.13] - 2025-08-02

### Changes

- Documentation
  - `README.md` updated
  - `docs/technical-overview.md` created

## [0.1.12] - 2025-07-27

### Changes

- Finalized **Notification** mechanism
- `EmailNotifier` added, sending via Google Email account
- Email template added

## [0.1.11] - 2025-07-26

### Changes

- For `interactive` mode, make `pooling_time` configurable either from command-line or from config file.
  The value from command-line takes precedence over the value from the config file.
- Make print of the program more descriptive (add some descriptions, remove temporary ones)
- Unify code of `interactive` and `oneshot` modes as they do exactly the same (so no need to duplicated code)

## [0.1.10] - 2025-07-26

### Changes

- Refactoring all Persistence Engines to comply with a new structure of the data

## [0.1.9] - 2025-07-25

### Changes

- Add **SQLite** as a Persistence Engine
  - All relevant classess and logic
  - SQL scripts for creating structure

## [0.1.8] - 2025-07-25

### Changes

- Add **MySQL** as a Persistence Engine
  - All relevant classess and logic
  - SQL scripts for creating structure
  - `docker-compose.yml` file for MySQL

## [0.1.7] - 2025-07-25

### Changes

- New Configuration mechanism:
  - Splitting into 3 parts: `GeneralConfig`, `PersistenceConfig`, `NotificationConfig`

## [0.1.6] - 2025-07-24

### Changes

- First, rough version of **Notification** mechanism:
  - module `notifier` created
  - `notifier.py` for **Notifier** class
  - `console_notifier.py` and `file_notifier.py` for **ConsoleNotifier** and **FileNotifier** classess respectively

## [0.1.5] - 2025-07-24

### Changes

- Make `utils` a module
- Add `ContentComparer` insite `utils` module class that consists a logic of comparison two strings
  and returns only added elements in the newer string

## [0.1.4] - 2025-07-24

### Changes

- Make `PersistenceEngineType` a string Enum
- Remove temporary config files and unify configuration into one `config.yaml` file
  with various Persistence Engine configuration examples

## [0.1.3] - 2025-07-24

### Changes

- Add refactoring of code, affecting modules `page`, `parser`, `persistence`
  - Create modules for this code
  - Split classess from one file into separate files
  - refactor all relevant files to user these modules directly (no long referencing names)

## [0.1.2] - 2025-07-05

### Changes

- Add PostgreSQL as a Persistence Engine `[#6]`
- Add new library dependence `psycopg[binary]`
- Add `docker-compose.yml` for PostgreSQL and PgAdmin4

## [0.1.1] - 2025-07-04

### Changes

- All code moved from `code` folder to `snooplyze` folder `[#3]`

### Fixes

- Wrong parameter name used in the code `pool-time`, should be `pooling-time` `[#4]`

## [0.1.0] - 2025-07-04

### Changes

- First `a-kind-of-working` version ;)
- Revamping structure of the project.
- Finalize 1st version of proper Persistence Layer (for now for DuckDB)
  - structure of DB is now taken from a script
  - adding functions that operate on Persistence Engine
- Add `fetch-type` parameter
  - `interactive` : run app and re-run the logic every `pooling-time` seconds (so no ned to schedule via external scheduling app)
  - `oneshot` : run app only once (so that it can be schedule from external scheduling app)
- Add `PageContent` class in order to handle the returned Content of the Page
- Move Python Virtual Environment to `.venv` folder instead of `snooplyze` folder

## [0.0.2] - 2025-06-12

### Changes

- Separate class **PersistenceLayerSetup** (_setup.py_) for setup persistence layer that is dependable on the engine
- FlatFile added as a Persistence Engine (**FlatFilePersistenceEngine** class)
- **add_content** method added to Persistence Engine
- **CLI** added for the app (for now based on argparse)

## [0.0.1] - 2025-06-08

### Changes

- Hello World!
- First working code.
- Code base divided into folders - first structure
- Classes **Page** and **PageMonitor** added.
- Classes **Parser** (abstract class) and **AllDocumentParser** **MainElementParser** **DivClassParser** added.

### Fixes
