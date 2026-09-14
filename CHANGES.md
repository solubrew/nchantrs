# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] — 2026-09-12 (T-NEW-167 card-number reservation)

### Fixed

- **WebEnginePage.createWindow now walks page → engine → viewer**
  when looking up `links_in_place` (was: engine only). The Jupyter
  notebook view sets the flag on the viewer cfg; in some install
  paths the engine `config.dikt` did not inherit the flag at the
  exact moment `createWindow` fired, so the handler fell through
  to `super().createWindow` ("default handling"), which returned
  a NULL page and triggered JupyterLab's
  `Cannot read properties of null (reading 'updateRenderOption')`.
  The walk now consults every node in the chain, and tolerates
  both the QObject-parent method shape and the Python-attribute
  shape set in `NchantdWebEngineView.__init__`. Tests in
  `tests/test_links_in_place_propagation.py` (8 cases).

## [Unreleased] — 2026-09-12 (T-NEW-167 card-number reservation)

### Notes

- **T-NEW-167 reserved for ad telemetry** in the T-NEW card
  namespace (shared with `nchantdoffice_com` + `nchantdoffice`).
  No source code change in this repo — the emitter lives in
  `nchantdoffice/nchantdoffice/widgets/documents/atnrg/ad_telemetry.py`
  and the ingest blueprint in
  `nchantdoffice_com/nchantdoffice_com/app/routes/ad_telemetry.py`.
  This row exists so the cross-repo sweep doc knows the number
  is taken.

## [Unreleased] — 2026-09-12 (slim-ad rotation landing + Get Pro interception)

### Added
- **`tests/test_browser_ncho_interception_tnew165.py` (`7cbf413`)** —
  9 AST-shaped checks pinning the Ad tab's `ncho://` interception
  wiring in `nchantdoffice/widgets/documents/atnrg/browsers.py`:
  - `_NchoInterceptionPage(NchantdWebEnginePage)` subclass exists
  - `acceptNavigationRequest` override returns `False` for `ncho://`
  - `_ncho_action_handlers` registry has the `open_settings` →
    `self._open_settings_node` mapping
  - `_install_ncho_interception_page` method is on `NchantdOfficeAdTab`
  - Page is wired via `self.engine.setPage(...)`
  - `NCHANTDOFFICE_OPEN_SETTINGS_LAUNCHER` / `switch_to_account_tab`
    handler is referenced
- **T-NEW-069 follow-up (`ad7c63a` style row)** — see prior
  [Unreleased] block: the empty-`active_url` clobbering fix that
  pinned the Ad tab on stack3 is now superseded by T-NEW-164's
  server-side rotation landing on `origin/gamma`.

### Changed
- The Ad tab's WebEngine page is now swapped at `initView` time
  (per nchantdoffice `5d334b9`) so `_NchoInterceptionPage` replaces
  the default `NchantdWebEnginePage` only on the slim-ad surface.
  Other web viewers are unaffected.
- Password dialog authentication flow in NchantdCape
- Detailed logging to trace initView and _show_password_dialog
- 12 new AST-only test files covering previously untested modules (2026-08-29):
  - `widgets/test_groups.py`, `widgets/test_embeds.py`, `widgets/test_calendars.py`,
    `widgets/test_canvases.py`, `widgets/test_launch.py`
  - `services/test_bonds.py`, `services/test_directories.py`
  - `utilities/test_formatting.py`, `utilities/test_files.py`
  - `dialogs/test_new.py`, `dialogs/test_search.py`, `dialogs/test_save.py`
- `subtrix` installed via shieldface and made available in nchantrs test env via `.pth` file

### Changed
- Refactored auth code to single auth flow in initView()
- Force authentication - always show password dialog
- `tests/conftest.py`: `mock_external_dependencies` now provides a real `uuid.uuid4().hex` stub
  for `subtrix.uuid_generator` (persisted outside `patch.dict` context so it survives function-scope)
- `tests/unit/nchantrs/services/conftest.py`: created — overrides session-scoped `mock_pyqt`
  with no-op for tags subtree (avoids Qt hang during headless collection/execution)

### Fixed
- **T-NEW-069 empty-`active_url` blanking (`af7c19e`, 2026-09-12)** — the Ad tab rendered
  blank after rotation. Live log showed `Load Document: <correct stack3 url>` followed 9ms
  later by `first show -> loading active_url ''` → `engine.load('')`, clobbering the page
  `_load_ad_layout` had already loaded. Root cause: `NchantdURL` subclasses `QUrl`, so
  `set_url_path`'s `isinstance(url, QUrl)` branch fired before the `NchantdURL` branch and
  read the wrapper's (empty) QUrl internal state instead of the authoritative `.url`
  attribute. Fixes: (1) `set_url_path` checks `NchantdURL` first, falls back to `toString()`
  only when `.url` is empty, and bails out when normalisation yields `''` (no history entry,
  no `active_url` clobber); (2) `showEvent` first-load requires a non-empty `.url` string —
  when empty it keeps the engine's already-loaded page (AdTab pre-loads before show), else
  falls back to `cmd_goto_page()`. Restored Ad tab on live desktop; rotation verified.
- **T-NEW-069 `populate_document` Viewer alias (`1a0c23c`, 2026-09-11)** — hoisted the
  cross-repo navigation contract alias (`populate_document(url)`) from the `NchantdWebBrowser`
  subclass to the `NchantdWebViewer` base class so the Ad tab's direct viewer calls
  (`_load_ad_layout` → `viewer.populate_document(url)`) resolve. With the alias only on the
  Browser, viewer-level calls raised `AttributeError` which was silently swallowed, leaving
  the tab blank with no error.
- **T-NEW-069 URL dropdown + history wiring (`8f0db6b`, 2026-09-11)** — `set_url_path`
  now tracks every navigation in a deduped most-recent-first `url_history` (capped at
  `url_history_max`, default 20) and syncs the URL dropdown (`update_options(replace=True,
  sort=False)` + `setCurrentText`). `NchantdWebBrowser.set_url_path` delegates to the
  Viewer's implementation (no double-sync). `save()` snapshot persists history via
  `_to_dict()`.
- **42 pre-existing test failures resolved** (`7e2ceec`, 2026-08-29):
  - `services/services.py`: `NchantrsService.__init__` now calls `super().__init__("NchantrsService", cfg)`
  - `models/models.py`: `set_instance_setting`/`save_instance_settings` unstubbed; `store_app_profile`
    implemented with `_store()` + validation
  - `services/tags.py`: uses `subtrix.uuid_generator()`; `rename()` now actually updates `self.name`
  - `widgets/browsers/browsers.py`: `NchantdWebViewer` gains `save()` + `_to_dict()`
  - `widgets/tables/tables.py`: `NchantdGrid` gains `add_grid_widgets()` helper
  - 6 test files updated to match actual API surfaces
- **H25 — Catalog Tab Wrong Child Count** (`commit fa05530`): `NchantdNode.loadChildren()` in
  `widgets/items/nodes.py` now consistently uses `pid_txt` field for parent filtering instead of
  mixing `parentid` and `pid_txt`. Fixes incorrect child counts across all node types including
  catalogs. (nchantdoffice consumer bug H25)
- **H29 — Tree Node Drag-and-Drop Regression** (`commit fa05530`): `NchantdNode.initModel()` in
  `widgets/items/nodes.py` now stores the full node dict in `Qt.UserRole` for drag-drop operations.
  Previously only stored a string, breaking `getNid()` in downstream consumers. (nchantdoffice
  consumer bug H29)
- **H30 — `setData()` Argument Order** (`commit 5afde9d`): `NchantdNode.initModel()` in
  `widgets/items/nodes.py:380` now calls `self.setData(0, Qt.UserRole, self.node)` — the
  correct argument order is `(column, role, value)`. Previously the args were inverted,
  storing the role ID in column 0, which silently failed and produced empty `UserRole` data.
  This compounded with H29 to break drag-and-drop in nchantdoffice.
- **H31 — `self.parent` Shadowing `QTreeWidgetItem.parent()`** (`commits 57839d2 + be8a582`):
  All `QTreeWidgetItem` subclasses (`NchantdItem`, `NchantdTreeItem`, `NchantdTreeNode`,
  `NchantdTree`) had `self.parent = parent` in their constructors, which shadowed Qt's built-in
  `parent()` method. This caused `TypeError: 'NchantdOfficeTreeNode' object is not callable`
  (and the equivalent for nchantrs node types) whenever Qt called `.parent()` on a tree item —
  most visibly in drag-and-drop `_is_descendant()` checks. Renamed all occurrences of
  `self.parent` → `self.parent_widget` across `widgets/items/items.py`,
  `widgets/items/nodes.py`, and `widgets/trees.py`.
- Duplicate auth code removed, single auth flow implemented
- logma.off() causing dialogs not to show (commits b5d5e92 + 1931cf5)
- Checkable attribute bug in `toolbars.py:switch_to_toggle()` - added safety checks to prevent double-call
- call initView() in NchantdCape.__init__

### Test Suite Status
- **666 passed, 5 skipped, 0 failed** (as of `82b3fb7`, 2026-08-29)
- Prior: 611 passed, 42 failed, 5 skipped
- 5 skipped tests in `test_widget_mixin_metaclass.py` require `--noconftest` (metaclass + MagicMock QObject incompatibility)

---

## [0.0.1] - 2026-01-15

### Added
- Core PyQt5/PySide6 GUI Framework
- NchantdStore - SQLite-backed data storage layer (extends MicroStash -> SQuiRL)
- Base model classes (PantiesModel, CloakModel, SigilModel)
- NchantdTheme - YAML + QSS theme management system
- GlainMixin - Optional glain integration for agent memory
- Widget system (Base NchantdWidget with config, theming, and lifecycle)
- Extension system - Plugin architecture
- Entry points: aberration, distortion, nchantment, flection
- Multi-pane (Cloak) implementation with tabbed/docked windows
- Web browser widgets (NchantdBrowser)
- Terminal widget with full ANSI escape sequence support
- Navigation stack using native QWebEngineHistory
- URL tracking via LinkService integration
- Session persistence with persistent cookies

### Changed
- Upgraded terminal widget to support full ANSI escape sequences (colors, bold, italic)
- Replaced manual deque navigation stacks with native QWebEngineHistory
- Simplified NchantdWebManager by switching from QThread to QObject
- Synchronized NchantdWebViewer with underlying browser signals
- Updated shell environment with TERM=xterm-256color and COLORTERM=truecolor
- Improved version parsing by converting components to integers
- Enhanced error handling in data operations (try-except blocks)
- Updated User-Agent for longer-lived Google sessions

### Fixed
- Fixed Login Session Handling - enabled persistent cookies and disk storage
- Fixed Browser Click Controls - middle-click for new tabs, context menus
- Fixed back/forward navigation by correctly emitting backAvailable/forwardAvailable signals
- Critical flaws in database migration - version comparison and sequential update application
- '0.1.10' correctly recognized as newer than '0.1.2'
- Fixed `run_update_views` accessing wrong parent attribute
- Fixed YAML Parsing warnings - added empty configuration blocks
- Fixed AttributeError in LinkService - store_link instead of store_media
- Fixed GPU Info initialization warnings
- Fixed TypeError in NchantdWebBrowser.initModel - string URL handling
- Fixed null-check for app.model in get_important_urls
- Fixed "Release of profile requested but WebEnginePage still not deleted" warning
- Improved lifecycle management in NchantdWebEngineView
- Fixed vw document sql creation to include GROUP
- Fixed column creation update functionality with table rebuild and new data insert
- Fixed canvas not attaching to scrollbars
- Fixed tree node creation
- Fixed right side tabs
- Removed redundant `self.set_theme()` call in NchantdCloakView.initView()
- Fixed toolbox rendering issue - QToolBox without parent widget
- Fixed 500ms delayed selection of Home node after startup
- Fixed "Text Can't be parsed for Yaml" warnings
- Fixed "GPUInfo" initialization warning
- Fixed document sql creation to include GROUP

### Security
- Security and maintainability review completed
- Fixed critical vulnerabilities identified in review
- Cleaned up dead code
- Removed hardcoded credentials and API keys
- Implemented secure configuration management

### Documentation
- Comprehensive README.md with entry point table and examples
- STATE.md with architecture documentation
- IMPLEMENTATION.md with developer guidance
- CONTRIBUTING.md with standard workflow

---

## [0.0.1] - Initial Release - 2025-12-01

### Added
- Initial project structure
- MVC/Cape-Cloak-Sigil pattern implementation
- Basic application templates
- Database schema with versioning system

[Unreleased]: https://github.com/solutionsbrewer/nchantrs/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/solutionsbrewer/nchantrs/releases/tag/v0.0.1
