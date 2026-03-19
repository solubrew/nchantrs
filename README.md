# Nchantrs

[![Python Version](https://img.shields.io/pypi/pyversions/nchantrs)](https://pypi.org/project/nchantrs/)
[![License](https://img.shields.io/pypi/l/nchantrs)](LICENSE)
[![Status](https://img.shields.io/pypi/status/nchantrs)](https://pypi.org/project/nchantrs/)
[![Downloads](https://img.shields.io/pypi/dm/nchantrs)](https://pypi.org/project/nchantrs/)

[![CI](https://github.com/solutionsbrewer/nchantrs/actions/workflows/ci.yml/badge.svg)](https://github.com/solutionsbrewer/nchantrs/actions)
[![codecov](https://codecov.io/gh/solutionsbrewer/nchantrs/branch/main/graph/badge.svg)](https://codecov.io/gh/solutionsbrewer/nchantrs)
[![Code Quality](https://img.shields.io/badge/code%20quality-95%25-success)](https://github.com/solutionsbrewer/nchantrs)

[![PyPI Version](https://img.shields.io/pypi/v/nchantrs)](https://pypi.org/project/nchantrs/)
[![Python Versions](https://img.shields.io/pypi/pyversions/nchantrs)](https://pypi.org/project/nchantrs/)

Nchantrs is a Python module for rapidly creating PyQt5/PySide6 applications using YAML configuration and Python widget files. Applications are built over a SQLite backend using FxSQuiRL for database operations.

## Features

- **4 Entry Points**: Choose the right architecture for your app (aberration, distortion, nchantment, flection)
- **YAML-Based Configuration**: Define application structure, UI layouts, widgets, and database schemas
- **Python Widget Files**: Extend functionality with custom widgets, events, and logic
- **PyQt5/PySide6 Integration**: Cross-platform desktop GUI framework support
- **SQLite Backend via FxSQuiRL**: Seamless database operations with one or more SQLite databases
- **Theme System**: Built-in theming with customizable QSS templates
- **Authentication**: Built-in password dialog and user authentication
- **Model-View Architecture**: Clean separation of concerns (Cape/Cloak/Sigil pattern)

## Installation

You can install Nchantrs via pip:

```bash
pip install nchantrs
```

Alternatively, clone the repository and install from source:

```bash
git clone https://github.com/<USER_OR_ORG>/nchantrs.git
cd nchantrs
pip install -e .
```

### Requirements

- Python 3.10 or higher
- PyQt5, PyQt6, or PySide6
- Dependencies: pyyaml, sqlalchemy, fxsquirl, condor, ogma, pycurity

## Quick Start

### Choose Your Entry Point

Nchantrs provides 4 entry points depending on your app's complexity:

| Entry Point | Use When | Backend |
|-------------|----------|---------|
| **aberration** | Simple dialogs, popups | None |
| **distortion** | Single-pane tools/utilities | YAML + SQLite |
| **nchantment** | Multi-pane office applications | SQLite + YAML |
| **flection** | Networked/P2P applications | SQLite + YAML + P2P |

### Basic Usage

```python
import nchantrs

# Choose the right entry point for your app:
# - aberration: Simple popup dialogs
# - distortion: Single-pane tool apps (YAML-first)
# - nchantment: Multi-pane office apps (SQLite-first)
# - flection: Networked apps with P2P

# For a distortion (single-pane tool) app:
from nchantrs.dialogs.distortion import NchantdDistortion

app = NchantdDistortion()
app.initModel()    # Initialize YAML/SQLite backend
app.initView()     # Set up UI
app.run()          # Start application
```

## Usage

### Loading Configurations

Nchantrs uses YAML files to define the app's UI and database interactions. A sample YAML might look like:

```yaml
app_name: MyApp
ui:
  main_window:
    title: Main Window
    widgets:
      - type: button
        label: Submit
        on_click: custom_handler
database:
  schema: path/to/schema.sql
  connections:
    - name: primary
      file: database.db
```

Use `nchantrs.load_config(yaml_path)` to parse and validate the config.

### Creating Applications

```python
# Load config
config = nchantrs.load_config('app.yaml')

# Specify widget directory
app = nchantrs.Application(config, widget_dir='widgets/')

# Add custom widget logic from Python files
app.register_widget('custom_widget.py')

# Initialize database with FxSQuiRL
app.init_database(config['database']['connections'][0]['file'])

# Execute queries
results = app.query('SELECT * FROM <TABLE_NAME>')
```

### Database Interactions

Leverage FxSQuiRL for SQLite operations:

```python
# Write data
app.insert('INSERT INTO <TABLE_NAME> (column) VALUES (?)', ('value',))

# Read data
data = app.fetch('SELECT * FROM <TABLE_NAME> WHERE id = ?', (1,))
```

### Supported Frameworks

- PyQt5
- PyQt6
- PySide2
- PySide6

## Examples

### Example 1: Simple CRUD Application

```python
import nchantrs

config = nchantrs.load_config('crud_app.yaml')
app = nchantrs.Application(config, widget_dir='crud_widgets/')
app.init_database('crud.db')

# Add a form widget for data entry
app.add_form('user_form', fields=['name', 'email'])

# Run with event loop
app.run()
```

### Example 2: Multi-Database Dashboard

```python
import nchantrs

config = nchantrs.load_config('dashboard.yaml')
app = nchantrs.Application(config, widget_dir='dashboard_widgets/')

# Connect to multiple databases
app.init_databases(['db1.db', 'db2.db'])

# Display data in UI
app.update_table('dashboard_table', query='SELECT * FROM metrics')

app.run()
```

## Configuration Guide

Each YAML config must include:

- `app_name`: String identifier for the application
- `ui`: Dictionary defining windows, widgets, layouts, and events
- `database`: Details for SQLite connections, schemas, and FxSQuiRL settings
- `widgets`: Optional mappings to Python files for custom logic

For advanced customization, refer to the [docs/config-reference.md](docs/config-reference.md).

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/<FEATURE_NAME>`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/<FEATURE_NAME>`).
5. Open a Pull Request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

## License

This project is licensed under the <LICENSE_TYPE> License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with inspiration from open-source GUI and database communities.
- Thanks to contributors of underlying libraries like <PYQT_LIB>, FxSQuiRL.