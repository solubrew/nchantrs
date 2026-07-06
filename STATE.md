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
| **Last Updated** | 2026-06-22 |

### Purpose
Nchantrs is a Python module for rapidly creating PyQt5/PySide6 applications using YAML configuration and Python widget files. Applications are built over a SQLite backend using FxSQuiRL.

---

## Recent Activity (2026-06-22)

### Latest Commits
| Commit | Description |
|--------|-------------|
| `c6bc679` | Add debug utilities module for data source dumps |
| `62f84c4` | Fix: call initView() in NchantdCape.__init__ |
| `adae9c8` | Add critical logging to trace initView and _show_password_dialog |
| `534570f` | Force authentication - always show password dialog |
| `e3b5a09` | Add detailed auth logging to NchantdCape.initView |
| `298c147` | Add password dialog to NchantdCape before loading widget |

### Latest Features
| Feature | Status | Description |
|---------|--------|-------------|
| **Debug Utilities** | ✅ NEW | `nchantrs/utilities/debug.py` - DataSourceDumper for inspecting store/model state |
| **Authentication Flow** | ✅ NEW | Password dialog in NchantdCape initView() |

### Known Issues
| Issue | Status | Description |
|-------|--------|-------------|
| **Auth Bug** | ✅ FIXED | Duplicate auth code removed, single auth flow in initView() |
| **logma.off() causing dialogs not to show** | ✅ FIXED | Commits b5d5e92 + 1931cf5 - Requires reinstall on test machine |
| **Checkable attribute bug** | ✅ FIXED | `toolbars.py:switch_to_toggle()` - added safety checks to prevent double-call |
| **syntax.py remaining FIXMEs** | 🟡 Pending | Some FIXMEs remain after commit 1931cf5 |
| **Deprecated dependencies** | ✅ FIXED | Cleaned pyproject.toml - removed 30+ obsolete packages |
| **Python version** | ✅ FIXED | Bumped from >=3.6 to >=3.10 |

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
  ├── NchantdCapeModel (Simple dialog applications) → distortion
  ├── NchantdCloakModel (Multi-pane applications) → nchantment/flection
  └── NchantdSigilModel (Dialog windows within applications) → aberration
```

### Entry Points
| Entry Point | Use Case | Backend | Example Apps |
|-------------|----------|---------|---------------|
| **aberration** | Standalone dialogs | None | Popups, simple forms |
| **distortion** | Single-pane tools | YAML + SQLite | nchantdaxn, settings editor |
| **nchantment** | Multi-pane office apps | SQLite + YAML | Office suites, IDEs |
| **flection** | Networked/P2P apps | SQLite + YAML + P2P | Chat, collaborative tools |

### Key Classes
| Class | Purpose |
|-------|---------|
| **NchantdCape** | Main dialog window container |
| **NchantdCloak** | Multi-pane main window |
| **NchantdSigil** | Modal/non-modal dialog window |
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
│   └── debug.py               # Debug utilities (NEW)
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
| **kahndor** | Configuration management |
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
| YAML configs | ✅ Implemented | Via kahndor |
| Widget system | ✅ Implemented | Base NchantdWidget |
| Model classes | ✅ Implemented | Panties, Cloak, Sigil |
| GlainMixin | ✅ Implemented | Optional agent memory |
| Extension system | ✅ Implemented | Plugin architecture |
| Multi-pane (Cloak) | ✅ Implemented | Tabbed/docked windows |
| Authentication | ✅ Implemented | Password dialog in Cape |
| Debug Utilities | ✅ Implemented | DataSourceDumper for inspection |
| Terminal Widget | ✅ Implemented | Full ANSI escape sequence support |
| Web Browser Widgets | ✅ Implemented | NchantdBrowser with history |
| Navigation Stack | ✅ Implemented | Native QWebEngineHistory |
| Session Persistence | ✅ Implemented | Persistent cookies |

### Feature Roadmap
| Feature | Status | Priority |
|---------|--------|----------|
| Unit tests | ⏳ Pending | High |
| Documentation polish | ⏳ Pending | Medium |
| BREAKING_CHANGES.md | ⏳ Pending | Medium |

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
| **NchantdCape** | Core component | ✅ Stable |
| **NchantdCloak** | Core component | ✅ Stable |
| **NchantdOffice** | Reference implementation | ⏳ Pending |

---

## Upgrade Scope (2026-06-22)

### Scope Definition
| Item | Details |
|------|---------|
| **Scope** | nchantrs + nchantdoffice |
| **Breaking changes** | OK if documented |
| **Resolution target** | nchantdoffice (reference impl) |
| **Goal** | nchantrs = core codebase for Solutions Brewer products |

### nchantdoffice (Reference Implementation)
- 11 Python files
- Working tree/tab generation patterns
- DB-driven widget architecture
- NchantdCloak-based implementation

### nchantrs (Core Framework)
- 429 Python files
- 102 TODO/FIXME items
- 25 AXN-tracked tasks

---

## Documentation

### Required Documentation Files
| File | Purpose | Status |
|------|---------|--------|
| **STATE.md** | Project state and overview | ✅ This file |
| **CHANGELOG.md** | Changelog of all changes | ✅ Updated (2026-06-22) |
| **BREAKING_CHANGES.md** | Breaking changes only | ⚠️ Needs content |
| **README.md** | Project readme | ✅ Exists |
| **IMPLEMENTATION.md** | Developer guidance | ✅ Exists |
| **CONTRIBUTING.md** | Contribution workflow | ✅ Exists |
| **CLI.md** | Command reference | ✅ Exists |

---

## Testing

### Test Suite
- **Location**: `test_nchantrs/`
- **Framework**: pytest

### Test Status
| Category | Status |
|----------|--------|
| Functional tests | ✅ Present |
| Core tests | ⏳ Pending |
| Widget tests | ⏳ Pending |
| Dialog tests | ⏳ Pending |
| Integration tests | ⏳ Pending |

---

## Version History

| Version | Date | Status |
|---------|------|--------|
| **Unreleased** | 2026-06-22 | Current development |
| **0.0.1** | 2026-01-15 | Initial structured release |
| **Initial** | 2025-12-01 | Project inception |

---

*Last updated: 2026-06-22*
