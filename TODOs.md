# TODOs — nchantrs

> Auto-generated on **2026-08-29** from inline source markers (`# TODO`, `# FIXME`, `# HACK`, `# XXX`, `# BUG` across `.py` files).
> **Last Updated:** 2026-08-29
> **Branch:** gamma
> **HEAD:** `8aaf380` — "feat(NchantdStore): bridge enable_search + search + rebuild_search_index methods"
> **Scan:** 2026-08-29 — ~10 TODOs across 9 files. Most are aspirational/design questions, not blocking bugs.

## Real TODOs

| File | Line | Text | Priority |
|------|------|------|----------|
| `nchantrs/models/applicationmodels.py` | 602 | TODO: there is an opportunity here to stream line I'm sure however we must ensure that primary keys of the... | Design |
| `nchantrs/widgets/browsers/browsers.py` | 60 | TODO: Proper implementation of engine reuse and background loading | Low |
| `nchantrs/widgets/browsers/browsers.py` | 74 | # self.link_library = PyfficeURLLibrary(cfg) TODO must be implemented in the Nchantdoffice layer | Low |
| `nchantrs/widgets/browsers/browsers.py` | 352 | # TODO: DEBUG something is triggering a refresh that settles to duckduckgo instead of staying on the site | Debug |
| `nchantrs/widgets/browsers/browsers.py` | 716 | TODO: need to keep track of web addresses so that when a user logs into a service for a web app the link redirects | Low |
| `nchantrs/widgets/calendars/timelines.py` | 204, 226 | Class names (NchantdTODOCalendar, NchantdTODOEntryPane) — NOT TODOs | N/A |
| `nchantrs/widgets/catalogs.py` | 89 | # TODO implement dynamic sizing control based on screen/viewport size | Low |
| `nchantrs/widgets/controls/button_groups.py` | 217 | TODO: make this a checkable group? or maybe switch to a radio button? | Design |
| `nchantrs/widgets/forms/forms.py` | 78 | TODO: need to get max columns grid in order to span other fields | Low |
| `nchantrs/widgets/items/nodes.py` | 228 | NchantdTreeNode - TODO: is failing due to not accepting NchantdTreeItem to the NchantdTreeModel | High? |
| `nchantrs/widgets/media/charts/charts.py` | 543, 559 | ax = None #TODO fix | Low |
| `nchantrs/widgets/media/images.py` | 68 | #TODO this was causing non ratio locked scaling of images. testing to determine if any further changes are needed | Low |
| `nchantrs/widgets/tables/tables.py` | 665 | TODO: splice returned rows into self._data at their offset | Medium |
| `nchantrs/utilities/users.py` | 106 | #TODO implement rerun of the password dialog | Medium |

## Resolved since last scan

The following stale TODOs from the 2026-08-01 scan are already fixed or removed:

| Was | Now |
|-----|-----|
| `calculators.py:44` — number key routing | ✅ Fixed T-NEW-002 (2026-08-01) |
| `models.py:1152` — TODO edit name | ✅ Removed 2026-08-01 |
| `config.py:144` — hash policy | ✅ Removed 2026-08-01 |
| `tables.py:481` — \n longest section | ✅ Removed 2026-08-01 |
| `tabsets.py:469` — toolbox update | ✅ Removed 2026-08-01 |
| `items/nodes.py:696` — TODO 3 fix user | ✅ Removed 2026-08-01 |
| `views/treeviews.py:281` — TODO 0 last node | ✅ Removed 2026-08-01 |
| `widgets/widgets.py:1039` — long-term process | ✅ Removed 2026-08-01 |
| `applicationmodels.py:357,426,470,744` — path/save/version | ✅ Fixed T-NEW-003 (2026-08-01) |
| `sigil.py:80` — refactor methods | ✅ Fixed T-NEW-003 (2026-08-01) |
| `applications.py:317` — implement method | ✅ Removed 2026-08-01 |
| `browsers/pages.py:150,155` — context menu + hit test | ✅ Fixed T-NEW-004 (2026-08-01) |
| `tables/lists.py:173` — configurable bullet list | ✅ Fixed T-NEW-005 (2026-08-01) |
| `selectors.py:164,194,209` — sorting | ✅ Fixed T-NEW-005 (2026-08-01) |
| `help.py:69` — FAQ tree | ✅ Fixed T-NEW-008 (2026-08-01) |
| `media.py:63` — side-process data | ✅ Fixed T-NEW-008 (2026-08-01) |
| `catalogs.py:195,251` — tab.tid + left/right | ✅ Removed 2026-08-01 |
| `trees.py:592` — read depth | ✅ Fixed T-NEW-006 (2026-08-01) |
| `wizards/instances.py:69` — refactor NchantdInstance | ✅ Removed 2026-08-01 |
| `wizards/users.py:215` — PRO aspirational | ✅ Removed 2026-08-01 |
| `media/charts/charts.py` — 8 chart types broken | ✅ Fixed T-NEW-001 (2026-08-01) |
| Wizard stubs (add_page, etc.) | ✅ Fixed T-NEW-007 (2026-08-01) |

## T-NEW Cards (all resolved as of 2026-08-01)

All T-NEW-001 through T-NEW-012 are marked resolved in CHANGES.md.
The T-NEW-NNN cards below are historical only.

### T-NEW-001 — Charts 3D/advanced ✅
### T-NEW-002 — Calculator key routing ✅
### T-NEW-003 — App model path/save/version ✅
### T-NEW-004 — Browser context menu + hit test ✅
### T-NEW-005 — Editors sorting + config ✅
### T-NEW-006 — Catalog/tree data-model gaps ✅
### T-NEW-007 — Wizard method stubs ✅
### T-NEW-008 — Misc (side-process, FAQs) ✅
### T-NEW-009 through T-NEW-012 — All resolved

## Pre-existing test failures (42 failures, 580 passed)

These failures predate this review session and are not addressed here.
They appear to stem from source refactors not propagating to the test suite.

| Group | Count | Likely cause |
|-------|-------|-------------|
| `test_widget_mixin_metaclass.py` | 3 | metaclass + QTableWidget / QLabel interaction |
| `test_verify_password.py` | 1 | path to `nchantrs.utilities.users` changed |
| `test_store_app_profile.py` | 2 | `store_app_profile` method signature/impl changed |
| `test_services.py` (TestNchantrsService) | 11 | service class refactor |
| `test_tags.py` (TestTagGroup, TestTag) | 5 | tag class refactor |
| `test_grid_add_widget_nchantd_cell.py` | 2 | grid cell widget refactor |
| Other | ~18 | Various source refactors |

## NOTE comments (informational)

These are developer notes, not TODOs:

- `nchantrs/widgets/widgets.py:107` — TODO_CRIT_pyside6pandas_metaclass reference
- `nchantrs/widgets/widgets.py:89` — same reference
- `nchantrs/utilities/debug.py:116,123,127,129,131` — DEBUG function log lines
- `nchantrs/widgets/browsers/graphics.py:46,48` — NCHANTD_WEBENGINE_DEBUG_PORT env

## H## Tracker

| ID | Title | Status | Resolved in |
|----|-------|--------|-------------|
| H25 | Catalog Tab Wrong Child Count | ✅ 2026-07-12 | `fa05530` |
| H29 | Tree Node Drag-and-Drop Regression | ✅ 2026-07-12 | `fa05530` |
| H30 | `setData()` Argument Order | ✅ 2026-07-13 | `5afde9d` |
| H31 | `self.parent` shadowing `Qt.parent()` | ✅ 2026-07-13 | `57839d2` |

## Recent commits (gamma, since 2026-08-20)

| Commit | Description |
|--------|-------------|
| `8aaf380` | feat(NchantdStore): bridge enable_search + search + rebuild_search_index methods |
| `89362aa` | Merge remote-tracking branch 'local/gamma' into gamma |
| `58f70d1` | add auto save on focus change to Nchantd Script |
| `969f484` | fix(tests): resolve conflict markers in test_verify_password.py, fix path to users.py |
| `c0c1735` | fix(nchantrs): tolerate url_select_entry=None in populate_viewport (DESK T-NEW-059) |
| `0a4640d` | debug columns in models and widgets |
| `fbe77dc` | debug index creation |
| `4a6c729` | Merge remote-tracking branch 'local/delta' into gamma |
| `c965779` | refactor User and Instance initialization |
| `16dc79f` | browser refactor |
| `720205c` | browser refactor |
| `5e1999d` | fix(nchantrs): alias verify_pword as verify_password (T-NEW-151) |
| `4d7170b` | fix(nchantrs): implement store_app_profile persistence (T-NEW-162 part B nchantrs side) |

## Architectural facts (as of 2026-08-29)

- nchantrs is the base framework. nchantdoffice extends it.
- Entry points: `aberration`, `distortion`, `nchantment`, `flection`
- MRO pattern: `NchantdWidgetMixin` before `QWidget` in all widget classes
- All NchantdDialogs live in `nchantrs.dialogs`
- `NchantdTreeView` at `nchantrs/views/treeviews.py:38` owns `set_current_node(node)`
- `NchantdColor` is the nchantrs-native color device (replaced PyfficeColor 2026-08-01)
- `NchantdStore` bridges `enable_search`/`search`/`rebuild_search_index` to micromole.search
- `create_instance` in `wizards/instances.py` handles both library and install paths

## NOTE — Informational

- `nchantrs/nchantrs.py:103 — [NOTE] Pyularity integration - requires pyularity package to be installed`
- `nchantrs/dialogs/dialogs.py:50 — [NOTE] We do NOT call super().__init__() here because NchantdPanties`
- `nchantrs/dialogs/dialogs.py:434 — [NOTE] hasattr guard is necessary because NchantdSigil is used both as a`
- `nchantrs/widgets/browsers/browsers.py:105 — [NOTE] viewer is already parented to self`
- `nchantrs/widgets/browsers/browsers.py:561 — [NOTE] default_profile doesn't exist on self, but on QWebEngineProfile`
- `nchantrs/widgets/browsers/engines.py:271 — [NOTE] do NOT parent/interceptor here — the pool owns lifetime`
- `nchantrs/widgets/media/editors/code.py:152 — [NOTE] Add paths to language-specific linters.`
- `nchantrs/widgets/media/editors/entries.py:104 — [NOTE] setCheckable(True) is now handled by NchantdButton.initView()`
- `nchantrs/widgets/widgets.py:892 — [NOTE] Mixin comes before QWidget in MRO, but we must call QWidget.__init__ directly`
- `nchantrs/tests/unit/test_nchantrs_core.py:34 — [NOTE] Actual initialization requires Qt app context`

---

*Last auto-scan: 2026-08-29 — HEAD `8aaf380`.*
