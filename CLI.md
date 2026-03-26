# Nchantrs CLI Documentation

## Overview

Nchantrs provides a command-line interface for managing your applications, dialogs, widgets, and extensions.

## Installation

```bash
pip install nchantrs
```

## Usage

```bash
nchantrs [command]
```

## Commands

### Core Commands

- `nchantrs run` - Launch the Nchantrs application
- `nchantrs init` - Initialize a new Nchantrs project
- `nchantrs version` - Show version information

### Dialog Commands

- `nchantrs dialogs list` - List available dialogs
- `nchantrs dialogs show <name>` - Show a specific dialog
- `nchantrs dialogs create` - Create a new dialog

### Widget Commands

- `nchantrs widgets list` - List available widgets
- `nchantrs widgets info <name>` - Get widget information

### Extension Commands

- `nchantrs extensions list` - List installed extensions
- `nchantrs extensions install <name>` - Install an extension
- `nchantrs extensions uninstall <name>` - Uninstall an extension

## Options

- `-v, --verbose` - Enable verbose output
- `-h, --help` - Show help message
- `--version` - Show version

## Examples

```bash
# Show version
nchantrs version

# List all widgets
nchantrs widgets list

# Install an extension
nchantrs extensions install myextension
```

## Configuration

Configuration file: `nchantrs.yaml`

```yaml
app:
  name: Nchantrs
  version: 1.0.0
theme: default
debug: false
```

## Arguments

| Argument | Description | Type | Default |
|----------|-------------|------|---------|
| command | The command to run | string | None |
| --verbose | Enable verbose mode | flag | False |
| --help | Show help | flag | False |

## Exit Codes

- `0` - Success
- `1` - Error
- `2` - Invalid usage
