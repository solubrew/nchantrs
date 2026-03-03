# Nchantrs

Nchantrs is a Python module used to create PyQt5/PySide2 applications quickly by a combination of YAML configuration and Python widget files. These applications are built over a SQLite backend using the FxSQuiRL module to read and write to one or more SQLite databases. It streamlines the development of GUI applications with database integration, allowing developers to define UI layouts and behaviors declaratively while handling data persistence efficiently.

## Features

- **YAML-Based Configuration**: Define application structure, UI layouts, widgets, and database schemas using intuitive YAML files.
- **Python Widget Files**: Extend functionality with custom Python scripts for widgets, events, and logic.
- **PyQt5/PySide2 Integration**: Supports both PyQt5 and PySide2 for building cross-platform desktop applications.
- **SQLite Backend via FxSQuiRL**: Seamless reading and writing to SQLite databases using the FxSQuiRL module for query management and data operations.
- **Rapid Prototyping**: Quickly assemble apps by combining configs and widgets, reducing boilerplate code.
- **Multi-Database Support**: Handle interactions with one or more SQLite databases in a single application.
- **Event Handling and Customization**: Bind events and customize behaviors through YAML or Python overrides.

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

- Python 3.<MIN_VERSION> or higher
- Dependencies: pyyaml, <PYQT_LIB>, fxsquirl, sqlite3 (automatically installed via pip where applicable)

## Quick Start

Import the module, load a YAML configuration, and launch the application:

```python
import nchantrs

# Load YAML config for the application
config = nchantrs.load_config('path/to/app.yaml')

# Initialize the application with widgets and database
app = nchantrs.Application(config, widget_dir='path/to/widgets')

# Connect to SQLite database via FxSQuiRL
app.init_database('path/to/database.db')

# Run the application
app.run()
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
- PySide2
- Custom extensions via Python widgets

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