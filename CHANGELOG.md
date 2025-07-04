# Changelog

All notable changes to this project will be documented in this file.

## [0.1.1] - 2025-07-04

### Changes

- All code moved from `code` folder to `snooplyze` folder [#3]

### Fixes

- Wrong parameter name used in the code `pool-time`, should be `pooling-time` [#4]

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
