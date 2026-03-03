# STATE.md - Nchantrs

## Current State: Active Development

### Project
| Attribute | Value |
|-----------|-------|
| **Name** | Nchantrs |
| **Type** | PyQt5/PySide6 GUI Framework |
| **Branch** | arthr-ws (development) |
| **Location** | `/home/solubrew/.arthr/workspace/projects/nchantrs` |
| **Repository** | `file:///mnt/overse/SBST01/vein/GitVein/nchantrs.git` |
| **Last Updated** | 2026-03-03 |

### Purpose
Nchantrs is a Python module for rapidly creating PyQt5/PySide6 applications using YAML configuration and Python widget files. Applications are built over a SQLite backend using FxSQuiRL.

---

## Recent Activity (2026-03-03)

### Latest Commits
| Commit | Description |
|--------|-------------|
| `62f84c4` | Fix: call initView() in NchantdCape.__init__ |
| `adae9c8` | Add critical logging to trace initView and _show_password_dialog |
| `534570f` | Force authentication - always show password dialog |
| `e3b5a09` | Add detailed auth logging to NchantdCape.initView |
| `298c147` | Add password dialog to NchantdCape before loading widget |

### Known Issues
| Issue | Status | Description |
|-------|--------|-------------|
| **NchantdPyKey Auth Bug** | 🔴 Open | Empty dialog appears, password dialog not showing. Investigation ongoing in NchantdCape.initView() flow |

---

## Architecture

### Core Components
| Component | Description |
|-----------|-------------|
| **NchantdStore** | Data storage layer (extends MicroStash -> SQuiRL) |
| **NchantdModel** | Base model classes (PantiesModel, CloakModel, SigilModel) |
| **NchantdTheme** | Theme management system |
| **GlainMixin** | Optional glain integration for agent memory |

### Model Hierarchy
```
NchantdPantiesModel (Base)
  ├── NchantdCapeModel (Simple dialog applications)
  ├── NchantdCloakModel (Multi-pane applications)
  └── NchantdSigilModel (Dialog windows within applications)
```

### Key Classes
| Class | Purpose |
|-------|---------|
| **NchantdCape** | Main dialog window container |
| **NchantdCloak** | Multi-pane main window |
| **NchantdSigil** | Modal/非modal dialog window |
| **NchantdWidget** | Base widget with config, theming, and lifecycle |
| **NchantdStore** | SQLite-backed data storage |

---

## Directory Structure
```
nchantrs/
├── __init__.py
├── __main__.py
├── _data_/                    # Configuration and resources
│   ├── icons/                 # Icon assets
│   ├── themes/                # QSS theme files
│   └── themes.yaml            # Theme configuration
├── actions/                   # Action handlers
├── agents/                    # Agent integrations
├── dialogs/                   # Dialog windows (NchantdCape, NchantdSigil)
├── events/                    # Event handlers
├── extensions/                # Extension system
├── libraries/                 # Library utilities
├── library/                   # Library modules
├── models/                    # Data models
│   ├── applicationmodels.py   # App model classes
│   ├── treemodels.py          # Tree view models
│   └── stashmodels.py         # Storage models
├── services/                  # Service integrations
├── themes/                    # Theme system
│   ├── themes.py              # Theme management
│   ├── images.py              # Image handling
│   └── ...
├── updates/                   # Update handlers
├── utilities/                 # Utilities
│   ├── users.py               # User management
│   ├── policies.py            # Policy enforcement
│   ├── files.py               # File utilities
│   └── ...
├── views/                     # View components
├── widgets/                   # UI widgets
│   ├── widgets.py             # Base NchantdWidget
│   ├── browsers/              # Web browser widgets
│   ├── editors/               # Text editor widgets
│   ├── forms/                 # Form widgets
│   ├── lists/                 # List widgets
│   └── tables/                # Table widgets
└── wizards/                   # Wizard dialogs
```

---

## Theme System

### Components
| Component | Description |
|-----------|-------------|
| **NchantdTheme** | Main theme class |
| **Theme Config** | YAML-based (`_data_/themes.yaml`) |
| **QSS Templates** | `_data_/themes/*.qss` |
| **Icons** | `_data_/icons/` |
| **Palettes** | Primary, accent, highlight, background, foreground, system |

### Available Themes
- midnight_mist
- midnight_eruption
- (See `_data_/themes.yaml` for full list)

---

## Dependencies

### Core Dependencies
| Package | Purpose |
|---------|---------|
| **condor** | Configuration management |
| **subtrix** | Path mechanisms |
| **ogma** | Logging (Logma) |
| **pyqt / pyside6** | GUI framework |
| **squirl / fxsquirl** | SQLite ORM |
| **pycurity** | Security/encryption |
| **glain** | Agent memory (optional) |

### Version Requirements
- Python 3.10+
- PyQt5 or PySide6

---

## Features

### Implemented Features
| Feature | Status | Notes |
|---------|--------|-------|
| NchantdStore | ✅ Stable | SQLite-backed data storage |
| Theme system | ✅ Implemented | YAML + QSS based |
| YAML configs | ✅ Implemented | Via condor |
| Widget system | ✅ Implemented | Base NchantdWidget |
| Model classes | ✅ Implemented | Panties, Cloak, Sigil |
| GlainMixin | ✅ Implemented | Optional agent memory |
| Extension system | ✅ Implemented | Plugin architecture |
| Multi-pane (Cloak) | ✅ Implemented | Tabbed/docked windows |
| Authentication | 🔄 In Progress | Password dialog added |

### Feature Roadmap
| Feature | Status | Priority |
|---------|--------|----------|
| Authentication flow | 🔄 In Progress | High |
| NchantdPyKey integration | 🔄 In Progress | High |
| Unit tests | ⏳ Pending | Medium |
| Documentation | ⏳ Pending | Medium |

---

## GitVein

### Repository
- **URL**: `file:///mnt/overse/SBST01/vein/GitVein/nchantrs.git`
- **Branches**:
  - `gamma` - Stable release branch
  - `arthr-ws` - Active development

### Workflow
1. Development happens on `gamma`
2. Merged to `arthr-ws` for testing
3. Testing completes → merge back to `gamma`

---

## Related Projects

### Parent/Child Relationships
| Project | Relationship | Status |
|---------|--------------|--------|
| **NchantdPyKey** | Child app | 🔴 Auth bug open |
| **NchantdCape** | Core component | ✅ Stable |
| **NchantdCloak** | Core component | ✅ Stable |
| **NchantdOffice** | Parent app | ⏳ Pending |

---

## Documentation

### Required Documentation Files
| File | Purpose | Status |
|------|---------|--------|
| **STATE.md** | Project state and overview | ✅ This file |
| **CHANGES.md** | Changelog of all changes | ✅ Exists |
| **BREAKING_CHANGES.md** | Breaking changes only | ❌ Missing |
| **README.md** | Project readme | ✅ Exists |

---

## Testing

### Test Suite
- **Location**: `test_nchantrs/`
- **Framework**: pytest

### Test Status
| Category | Status |
|----------|--------|
| Core tests | ⏳ Pending |
| Widget tests | ⏳ Pending |
| Dialog tests | ⏳ Pending |
| Integration tests | ⏳ Pending |

---

*Last updated: 2026-03-03*
