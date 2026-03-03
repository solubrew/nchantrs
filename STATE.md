# STATE.md - Nchantrs

## Current State: Active Development

### Project
- **Name**: Nchantrs
- **Type**: PyQt5/PySide6 GUI Framework
- **Branch**: arthr-ws
- **Location**: /home/solubrew/.arthr/workspace/projects/nchantrs
- **Repository**: file:///mnt/overse/SBST01/vein/GitVein/nchantrs.git

### Purpose
Nchantrs is a Python module for rapidly creating PyQt5/PySide6 applications using YAML configuration and Python widget files. Applications are built over a SQLite backend using FxSQuiRL.

### Architecture

#### Core Components
| Component | Description |
|-----------|-------------|
| **NchantdStore** | Data storage layer (extends MicroStash -> SQuiRL) |
| **NchantdModel** | Base model classes (PantiesModel, CloakModel, SigilModel) |
| **NchantdTheme** | Theme management system |
| **GlainMixin** | Optional glain integration for agent memory |

#### Model Hierarchy
```
NchantdPantiesModel (Base)
  ├── NchantdCapeModel (Simple dialog applications)
  ├── NchantdCloakModel (Multi-pane applications)
  └── NchantdSigilModel (Dialog windows within applications)
```

#### Directory Structure
```
nchantrs/
├── actions/        # Action handlers
├── agents/         # Agent integrations
├── dialogs/        # Dialog windows
├── events/         # Event handlers
├── extensions/     # Extension system
├── libraries/      # Library utilities
├── library/        # Library modules
├── models/         # Data models (NchantdStore, applicationmodels, treemodels)
├── services/       # Service integrations
├── themes/         # Theme system (themes.py, images.py)
├── updates/        # Update handlers
├── utilities/      # Utilities (users, policies, files, etc.)
├── views/          # View components
├── widgets/        # UI widgets
└── wizards/        # Wizard dialogs
```

#### Theme System
- **NchantdTheme**: Main theme class
- **Theme Config**: YAML-based (`_data_/themes.yaml`)
- **QSS Templates**: `_data_/themes/*.qss`
- **Icons**: `_data_/icons/`
- **Palettes**: Primary, accent, highlight, background, foreground, system

#### Dependencies
| Package | Purpose |
|---------|---------|
| condor | Configuration management |
| subtrix | Path mechanisms |
| ogma | Logging (Logma) |
| pyqt / pyside6 | GUI framework |
| squirl / fxsquirl | SQLite ORM |
| pycurity | Security/encryption |
| glain | Agent memory (optional) |

### Features
| Feature | Status |
|---------|--------|
| NchantdStore | ✅ Stable |
| Theme system | ✅ Implemented |
| YAML configs | ✅ Implemented |
| Widget system | ✅ Implemented |
| Model classes | ✅ Implemented |
| GlainMixin | ✅ Implemented |
| Extension system | ✅ Implemented |
| Multi-pane (Cloak) | ✅ Implemented |

### GitVein
- **URL**: file:///mnt/overse/SBST01/vein/GitVein/nchantrs.git
- **Branches**: gamma (main), arthr-ws (development)

### Last Updated
2026-03-03
