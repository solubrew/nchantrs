# Implementation Guide

## Entry Points & Backend Architecture

The nchantrs framework provides four entry points, each representing different levels of network complexity and backend configuration:

### Overview

| Entry Point | Backend | Primary Storage | Secondary Storage | Network |
|-------------|---------|-----------------|-------------------|---------|
| **aberration** | None | None | N/A | None |
| **distortion** | YAML/SQLite | YAML | SQLite | None |
| **nchantment** | SQLite+YAML | SQLite | YAML | None |
| **flection** | SQLite+YAML | SQLite | YAML | P2P (ZMQ) |

### Configuration Storage

Both **distortion** and **nchantment** support configurations existing outside of the SQLite database:

- **distortion** (YAML/SQLite): Primary YAML files, optional SQLite for runtime data
- **nchantment** (SQLite+YAML): Primary SQLite, with YAML config files outside the database

This allows flexibility in how applications store their configuration:

```
nchantdaxn/
├── config.yaml          ← YAML config (outside DB - distortion)
├── data.db              ← Optional SQLite
└── ...

# Or for nchantment:
nchantdoffice/
├── settings.db          ← SQLite (primary)
├── theme.yaml           ← YAML config (outside DB)
└── ...
```

### Choosing an Entry Point

| Use Case | Recommended Entry Point |
|----------|------------------------|
| No persistence needed | aberration |
| YAML-first, minimal SQLite | distortion |
| SQLite-first, YAML for external configs | nchantment |
| P2P networking required | flection |

### Quick Reference: When to Use Each Entry Point

#### aberration - Standalone Dialogs
Use for: Pop-up dialogs, simple input forms, notification windows
- No backend storage required
- Lightweight, single widget
- Examples: Color picker, file dialog, simple input

```python
# Example: Using aberration for a simple dialog
from nchantrs.dialogs.aberration import NchantdAberration

class MyDialog(NchantdAberration):
    def initWidget(self):
        self.setWidget(MyCustomWidget())
```

#### distortion - Single-Pane Tool Applications
Use for: Configuration tools, standalone utilities, data viewers
- YAML primary config, optional SQLite for runtime data
- Single main window (NchantdCape)
- Examples: nchantdaxn, settings editor, log viewer

```python
# Example: Using distortion for a tool app
from nchantrs.dialogs.distortion import NchantdDistortion

app = NchantdDistortion()
app.initModel()    # Initialize YAML/SQLite backend
app.initView()     # Set up single-pane UI
app.run()          # Start application
```

#### nchantment - Full Multi-Pane Office Applications
Use for: Complex apps with tabs, panels, multiple views
- SQLite primary storage, YAML for external configs
- Multi-pane window (NchantdCloak)
- Examples: Office suites, IDEs, complex data apps

```python
# Example: Using nchantment for an office app
from nchantrs.dialogs.nchantment import NchantdNchantment

app = NchantdNchantment()
app.initModel()    # Initialize SQLite + YAML backend
app.initView()     # Set up multi-pane UI with tabs/panels
app.run()          # Start application
```

#### flection - Networked/P2P Applications
Use for: Collaborative apps, real-time sync, distributed systems
- SQLite + YAML + P2P (ZMQ) networking
- Networked multi-pane window
- Examples: Chat apps, collaborative editors, distributed tools

```python
# Example: Using flection for a networked app
from nchantrs.dialogs.flection import NchantdFlection

app = NchantdFlection()
app.initModel()    # Initialize SQLite + YAML + P2P backend
app.initView()     # Set up networked multi-pane UI
app.run()          # Start application with P2P discovery
```

## Internal Projects Dependencies

Per CODING_STANDARDS, internal projects (kahndor, ogma, nchantrs, pycurity) should **NOT** be included as dependencies in `pyproject.toml`. They must be:

- Installed separately in the environment
- Imported directly where needed
- Documented in STATE.md as runtime dependencies

### Why?

There is an issue with internal projects being registered incorrectly even on install when listed in pyproject.toml dependencies.
