# Almora

Almora is a Python-based command-line interface (CLI) application and utility suite designed for managing custom scripts, alias commands, application configurations, and runtime execution contexts.

## Architecture and System Design

Almora is built following Clean Architecture principles, ensuring clear boundaries between CLI interaction, domain logic, settings management, and infrastructure handlers.

- **Application (`src/almora/app/`)**: Argument parsing (`cli.py`), command-line interfaces, and subcommand routers.
- **Core Settings (`src/almora/core/`)**: Configuration management (`settings.py`), Rich console themes (`config.py`), and staged setting item models (`settings2.py`) supporting `Switch`, `Selection`, `StringSettings`, and `IntSettings`.
- **Infrastructure (`src/almora/infrastructure/`)**: Environment directory initialization (`filesystem.py`) for `data/`, `logs/`, `.env`, and `settings.json`, alongside logging handlers (`logging.py`).
- **Models (`src/almora/models/`)**: Runtime session state (`SessionContext`) and user authentication state management (`UserContext`).
- **Utilities (`src/almora/utils/`)**: Data structure utilities (`data_utils.py`) for dictionary synchronization and list index resolution.

Detailed architectural documentation is available in [Architecture Overview](docs/architecture/overview.md) and [Module Breakdown](docs/architecture/modules.md).

## Requirements

- Python >= 3.14
- Virtual environment manager (`venv`)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/09pattt/almora.git
   cd almora
   ```

2. Create and activate a virtual environment:
   ```bash
   python3.14 -m venv .venv_dev
   source .venv_dev/bin/activate
   ```

3. Install project dependencies in editable mode with development tools:
   ```bash
   pip install -e .[dev]
   ```

## Usage

### Command-Line Interface

Invoke the CLI via the installed binary:

```bash
almora [options] [command] [subcommand]
```

Or via Python module execution:

```bash
python -m almora [options] [command] [subcommand]
```

### Options

- `-v`, `--version`: Show program version and exit.
- `-y`, `--yes`: Force upcoming interactive decisions to confirm.

### Subcommands

- `menu`: Open interactive menu interface (default command).
- `info`: Display system information. Options include:
  - `info status`: Output current application status.
  - `info settings`: Output configuration settings.
  - `info user`: Output user authentication status and profile.

## Development and Testing

### Running Tests

Execute the full pytest suite:

```bash
pytest
```

Run tests for specific components:

```bash
pytest tests/core/
pytest tests/app/
pytest tests/infrastructure/
```

## Documentation Directory

Additional project technical documentation is organized within `docs/`:

- [Documentation Index](docs/README.md)
- [Architecture Overview](docs/architecture/overview.md)
- [Module Breakdown](docs/architecture/modules.md)
- [Development Setup Guide](docs/development/setup.md)
- [Coding Conventions & Guidelines](docs/development/conventions.md)
- [Docstring Style Guide](docs/development/docstring_guide.md)
- [Git Workflow & Commit Guide](docs/development/git_workflow.md)
- [Changelog](docs/changelog.md)

## License and Maintainer

- **Author**: Napat Phonpattaranon (09pattt@gmail.com)
- **Repository**: [github.com/09pattt/almora](https://github.com/09pattt/almora)
