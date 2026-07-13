# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Debug utilities module (`nchantrs/utilities/debug.py`) - DataSourceDumper for inspecting store/model state
- Password dialog authentication flow in NchantdCape
- Detailed logging to trace initView and _show_password_dialog

### Changed
- Refactored auth code to single auth flow in initView()
- Force authentication - always show password dialog

### Fixed
- **H25 — Catalog Tab Wrong Child Count** (`commit fa05530`): `NchantdNode.loadChildren()` in
  `widgets/items/nodes.py` now consistently uses `pid_txt` field for parent filtering instead of
  mixing `parentid` and `pid_txt`. Fixes incorrect child counts across all node types including
  catalogs. (nchantdoffice consumer bug H25)
- **H29 — Tree Node Drag-and-Drop Regression** (`commit fa05530`): `NchantdNode.initModel()` in
  `widgets/items/nodes.py` now stores the full node dict in `Qt.UserRole` for drag-drop operations.
  Previously only stored a string, breaking `getNid()` in downstream consumers. (nchantdoffice
  consumer bug H29)
- Duplicate auth code removed, single auth flow implemented
- logma.off() causing dialogs not to show (commits b5d5e92 + 1931cf5)
- Checkable attribute bug in `toolbars.py:switch_to_toggle()` - added safety checks to prevent double-call
- call initView() in NchantdCape.__init__

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
