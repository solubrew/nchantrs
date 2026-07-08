# Nchantrs TODOs — Live Source of Truth

> **Last extracted:** 2026-07-08 via `extract_todos.py`
> **Source:** `git log -1 --format="%H %ai%n%an <%ae>%n%B"` → `478b41b` (solubrew, Wed Jul 8 18:27:40 2026)

---

## Recent Activity

| Date | Commit | Author | Summary |
|------|--------|--------|---------|
| 2026-07-08 | `478b41b` | solubrew | Firefox identity complete: UA + client-hints disable + navigator/window fingerprint overrides |
| 2026-07-08 | `bca7281` | solubrew | Keep full Firefox UA |
| 2026-07-08 | `deaa63d` | solubrew | Open new browser tab / switch to existing if URL matches |
| 2026-07-08 | `02d33ec` | solubrew | Restore soft-banner |
| 2026-07-08 | `56c51ce` | solubrew | Soft-banner baseline |
| 2026-07-08 | `41cbdf3` | orinbai | [nchantdoffice] overhaul TODOs.md to be source of truth |
| 2026-07-08 | `0598d13` | orinbai | [nchantdoffice] H24 fix: deferred toolbox refresh via QTimer.singleShot |
| 2026-07-08 | `59dc1e9` | solubrew | [nchantdoffice] browsers.py: open new browser tab; switch to existing if URL matches |

---

## Overview

- **49 inline TODOs** found across **21 files** (extraction date: 2026-07-08)
- Excludes test files from priority tracking (those TODOs are test scaffolding)
- Excludes `PROJECT_TRACKER.yaml` TODO items (those are linter/check configs, not code)
- Excludes `STATE.md` line 241 (old static count — superseded by this file)
- **18 priority items** in source files (categories: Critical, Browser, UI, Models, UX)

---

## Priority TODOs

### 🔴 Critical

#### `nchantrs/models/applicationmodels.py`
| Line | Priority | Text |
|------|---------|------|
| 470 | **TODO:0** | `return "0.0.1.0.1.4"` — need a better way to track updating the base version |

> Hardcoded version string. Needs a proper versioning scheme (semver, date-based, or git hash).

#### `nchantrs/models/applicationmodels.py`
| Line | Priority | Text |
|------|---------|------|
| 426 | TODO | `self.level = cfg.get("level")` — IMPLEMENT better for instance |

> Level tracking is stubbed. Needs a real implementation for instance-level hierarchy.

#### `nchantrs/models/applicationmodels.py`
| Line | Priority | Text |
|------|---------|------|
| 656 | TODO | There is an opportunity to streamline primary key tracking across the model |

> Primary key management could be refactored for consistency.

---

### 🟠 Browser

#### `nchantrs/widgets/browsers/browsers.py`
| Line | Priority | Text |
|------|---------|------|
| 58 | TODO | Proper implementation of engine reuse and background loading |

> QtWebEngine view creation is currently per-tab. Engine reuse could reduce memory and improve load times.

#### `nchantrs/widgets/browsers/browsers.py`
| Line | Priority | Text |
|------|---------|------|
| 114 | TODO | Change from browser/viewer to web app — use same engine but place it in a new Viewer subclass |

> Support for web-app mode: reuse WebEngine but with a different view subclass for richer integration.

#### `nchantrs/widgets/browsers/browsers.py`
| Line | Priority | Text |
|------|---------|------|
| 638 | TODO | Keep track of web addresses so user logins persist across sessions |

> Currently no URL-to-session mapping. Login state is not preserved for web apps.

---

### 🟡 UI / Widgets

#### `nchantrs/dialogs/dialogs.py`
| Line | Priority | Text |
|------|---------|------|
| 434 | TODO | `hasattr(self.app, "model")` — ensure this works; may need to switch to NchantdClip |

> The dialog app-reference check needs validation against actual runtime behavior.

#### `nchantrs/widgets/calendars/days.py`
| Line | Priority | Text |
|------|---------|------|
| 123 | TODO | `self.name = None` — get tab name |

> Calendar day tab name is not being set. Needs to resolve the tab name from the date.

#### `nchantrs/widgets/items/nodes.py`
| Line | Priority | Text |
|------|---------|------|
| 255 | TODO | `NchantdTreeNode` is failing — not accepting `NchantdTreeItem` to `NchantdTreeModel` |

> Tree node construction is broken. Needs debugging of model item acceptance.

#### `nchantrs/widgets/media/media.py`
| Line | Priority | Text |
|------|---------|------|
| 144 | TODO | Build in the ability to make the media button checkable |

> Media button should support toggle/checked state.

#### `nchantrs/widgets/media/images.py`
| Line | Priority | Text |
|------|---------|------|
| 224, 226 | TODO | Hardcoded `size_0 = 100`, `size_1 = 100` — calculate space dynamically |

> Image grid sizes are fixed; should be computed from available space.

#### `nchantrs/widgets/forms/forms.py`
| Line | Priority | Text |
|------|---------|------|
| 107 | TODO | Need to get max columns grid in order to span other fields |

> Form field spanning not implemented; grid column count must be known first.

---

### 🔵 UX / Controls

#### `nchantrs/widgets/controls/button_groups.py`
| Line | Priority | Text |
|------|---------|------|
| 262 | TODO | Make this a checkable group? Or switch to a radio button? |

> ButtonGroup behavior is ambiguous; should be either checkable multi-select or exclusive radio-style.

---

### 🟢 Models / Data

#### `nchantrs/models/_data_/treemodels.yaml`
| Line | Priority | Text |
|------|---------|------|
| 31 | TODO | Tree model not built out for full control as needed |

> Tree model definition is incomplete; full tree behavior not implemented.

#### `nchantrs/models/_data_/treemodels.yaml`
| Line | Priority | Text |
|------|---------|------|
| 141 | TODO | Tree model not built out for full control as needed |

> Same as above — second instance of incomplete tree model.

#### `nchantrs/models/tabsetmodels.py`
| Line | Priority | Text |
|------|---------|------|
| 218 | TODO | `tab_widgets[tabn].position = tabn` — move into tab object |

> Position tracking should be encapsulated in the tab class, not managed externally.

#### `nchantrs/models/tabsetmodels.py`
| Line | Priority | Text |
|------|---------|------|
| 249 | TODO | `cfg["file_path"] = cfg.get("file_path", cfg.get("path", ""))` — refactor source |

> Path field mapping is duplicated; refactor to a single source of truth.

#### `nchantrs/widgets/groups.py`
| Line | Priority | Text |
|------|---------|------|
| 429, 430, 436 | TODO HACK | Hardcoded scroll calculations: `viewport().size().width() * 2`, `setMaximum`, center position |

> Horizontal scroll hack needs a proper scrollable group layout.

---

### ⚪ Infrastructure / Services

#### `nchantrs/widgets/agents/agents.py`
| Line | Priority | Text |
|------|---------|------|
| 100 | TODO | 20240723 — create a dialog to monitor the status of the Sentinel |

> Sentinel agent needs a status monitoring dialog (stale from 2024-07-23).

#### `nchantrs/widgets/applications/applications.py`
| Line | Priority | Text |
|------|---------|------|
| 266 | TODO | `initModel()` eventually needs to be in a separate process |

> Application model init is synchronous; should be offloaded for large models.

#### `nchantrs/widgets/widgets.py`
| Line | Priority | Text |
|------|---------|------|
| 1039 | TODO | `if apps:` — not sure if we should keep this process long term |

> Process-heavy app discovery; may need to be re-evaluated.

#### `nchantrs/wizards/apps.py`
| Line | Priority | Text |
|------|---------|------|
| 530 | TODO | Controls for allowing the user to turn the library on but only for paid versions |

> Paid-tier gating for library feature not implemented.

---

### 🔧 Configuration

#### `nchantrs/utilities/_data_/templates.yaml`
| Line | Priority | Text |
|------|---------|------|
| 133 | TODO | `pid = '066a7cf6-5aca-7912-8000-4e27f26fd8c2'` — move to a config file |

> Hardcoded PID should be in a dedicated config file.

#### `nchantrs/models/applicationmodels.py`
| Line | Priority | Text |
|------|---------|------|
| 222 | TODO | `NchantdOfficeStickyNote` reference — shouldn't reference NchantdOffice from nchantrs |

> Cross-project reference needs to be resolved.

---

## Excluded (Test / Meta Files)

These files contain TODOs but are not production source code:

| File | Count | Notes |
|------|-------|-------|
| `tests/unit/nchantrs/test_app_todos.py` | 12 | Test scaffolding / example app TODOs |
| `PROJECT_TRACKER.yaml` | 8 | Linter check configs, not code |
| `STATE.md` | 1 | Old static count (superseded by this file) |

---

## Extracted Inline TODOs (Full Inventory)

```
nchantrs/dialogs/dialogs.py:434         # TODO ensure that this will work
nchantrs/models/_data_/treemodels.yaml:31  # TODO: this is not built out for full control
nchantrs/models/_data_/treemodels.yaml:141 # TODO: this is not built out for full control
nchantrs/models/applicationmodels.py:222   # TODO fix this shouldn't reference NchantdOffice
nchantrs/models/applicationmodels.py:426  # TODO: IMPLEMENT better for instance
nchantrs/models/applicationmodels.py:470  # TODO:0 need a better way to track version
nchantrs/models/applicationmodels.py:656  # TODO: streamline primary keys
nchantrs/models/tabsetmodels.py:218       # TODO move into tab
nchantrs/models/tabsetmodels.py:249       # TODO refactor source
nchantrs/utilities/_data_/templates.yaml:133  # TODO: move to a config file
nchantrs/widgets/agents/agents.py:100    # TODO: 20240723 create Sentinel dialog
nchantrs/widgets/applications/applications.py:266  # TODO eventually in a separate process
nchantrs/widgets/browsers/browsers.py:58  # TODO: Proper engine reuse
nchantrs/widgets/browsers/browsers.py:114 # TODO: web app Viewer subclass
nchantrs/widgets/browsers/browsers.py:638 # TODO: track web addresses for login persistence
nchantrs/widgets/calendars/days.py:123    # TODO get tab name
nchantrs/widgets/controls/button_groups.py:262  # TODO make checkable group?
nchantrs/widgets/forms/forms.py:107       # TODO need max columns grid
nchantrs/widgets/groups.py:429,430,436   # TODO HACK: scroll calculations
nchantrs/widgets/items/nodes.py:255       # TODO: tree node failing
nchantrs/widgets/media/images.py:224,226  # TODO calculate space
nchantrs/widgets/media/media.py:144       # TODO make button checkable
nchantrs/widgets/widgets.py:1039          # TODO: not sure if keep long term
nchantrs/wizards/apps.py:530             # TODO paid version controls
```

---

*This file is the authoritative source of truth for inline TODOs. It supersedes any static counts in `STATE.md` or elsewhere. Update this file whenever TODOs are added, resolved, or modified.*
