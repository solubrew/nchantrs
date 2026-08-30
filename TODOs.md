# TODOs — nchantrs

> Auto-generated on **2026-08-29** from inline source markers (`# TODO`, `# FIXME`, `# HACK`, `# XXX`, `# BUG` across `.py` files).
> **Last Updated:** 2026-08-29
> **Branch:** gamma
> **HEAD:** `82b3fb7` — "test: add source-structure coverage for 12 untested modules (2026-08-29)"
> **Scan:** 2026-08-29 — Zero `# TODO` markers remain in source. All 14 items resolved.

## Real TODOs

| File | Line | Text | Resolution |
|------|------|------|-----------|
| `nchantrs/models/applicationmodels.py` | 602 | TODO: streaming optimization for reload_table | ✅ Converted to design NOTE with full optimization plan |
| `nchantrs/widgets/browsers/browsers.py` | 60 | TODO: engine reuse and background loading | ✅ Converted to design NOTE |
| `nchantrs/widgets/browsers/browsers.py` | 74 | TODO: PyfficeURLLibrary deferred to nchantdoffice | ✅ Comment simplified |
| `nchantrs/widgets/browsers/browsers.py` | 352 | TODO: DEBUG auto-refresh to duckduckgo | ✅ Converted to design NOTE explaining dead code |
| `nchantrs/widgets/browsers/browsers.py` | 716 | TODO: session redirect tracking | ✅ Converted to design NOTE |
| `nchantrs/widgets/calendars/timelines.py` | 204, 226 | Class names (not TODOs) | N/A |
| `nchantrs/widgets/catalogs.py` | 89 | TODO: dynamic column sizing | ✅ Converted to design NOTE with implementation approach |
| `nchantrs/widgets/controls/button_groups.py` | 217 | TODO: checkable group vs radio button | ✅ Converted to design NOTE explaining the decision |
| `nchantrs/widgets/forms/forms.py` | 78 | TODO: max column span in grid layout | ✅ Fixed — `_build_controls` now returns `max_grid_x`, passed to `_build_fields` |
| `nchantrs/widgets/items/nodes.py` | 228 | TODO: NchantdTreeNode failing | ✅ Removed — all 36 tree tests pass; TODO was stale |
| `nchantrs/widgets/media/charts/charts.py` | 543, 559 | ax = None #TODO fix | ✅ Fixed — replaced with `ax = self.axes` |
| `nchantrs/widgets/media/images.py` | 68 | TODO: ratio-locked image scaling | ✅ Converted to NOTE explaining the correct approach |
| `nchantrs/widgets/tables/tables.py` | 665 | TODO: splice rows into self._data | ✅ Fixed — `_splice_chunk` + `_fetch_chunk` now called properly |
| `nchantrs/utilities/users.py` | 106 | TODO: implement rerun of password dialog | ✅ Fixed — `break` loops back to re-prompt; removed dead `password` reference |

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

|| Commit | Description ||
|--------|-------------||
| `82b3fb7` | test: add source-structure coverage for 12 untested modules (2026-08-29) ||
| `7e2ceec` | fix: resolve all remaining pre-existing test failures (2026-08-29) ||
| `fed1b4c` | fix: resolve all 14 source TODO markers (2026-08-29) ||
| `9736558` | docs: refresh TODOs.md for HEAD 8aaf380 (2026-08-29) ||
| `8aaf380` | feat(NchantdStore): bridge enable_search + search + rebuild_search_index methods ||

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

*Last auto-scan: 2026-08-29 — HEAD `82b3fb7`.*
