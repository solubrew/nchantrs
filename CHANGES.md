# CHANGES.md - Nchantrs

All notable changes to the Nchantrs project will be documented in this file.

---

## [Unreleased] - v0.3.1

### Added
- CLI module (nchantrs/cli.py) for command-line interface
- `__main__.py` entry point for python -m execution
- Logging configuration in nchantrs/__init__.py
- nchantrs.yaml configuration file
- config/nchantrs.yaml configuration file (secondary location)
- CONTRIBUTING.md for contribution guidelines
- .github/workflows/ci.yml for CI/CD configuration
- CLI.md documentation with commands, arguments, and examples
- Additional CLI commands: actions, dialogs, events, models, services, utilities, widgets, wizards

### Changed
- Updated __init__.py with logging and version info
- Expanded CLI to cover all 10 modules

### Fixed
- Added missing QCursor import (a725161)
- Fixed parent() call on widget with no parent set (c100a97)
- Check for QApplication.model and set None instead of error (fb52407)
- Remove redundant welcome label blocking AXNTask (8a7ebcc)
- Add Projects tab to NchantdAXN - Tasks, Projects tab (c7b18fa)
- Initialize placeholder variable before log line (3f406da)
- Add init() classmethod to NchantdCape for CLI (cb4aa56)
- Add AXN task list pane to NchantdCape (38d305b)

### Fixed
- Added missing QCursor import (a725161)
- Fixed parent() call on widget with no parent set (c100a97)
- Check for QApplication.model and set None instead of error (fb52407)
- Remove redundant welcome label blocking AXNTask (8a7ebcc)
- Add Projects tab to NchantdAXN - Tasks, Projects tab (c7b18fa)

### Security
- Phase 1-5 Upgrade: Security, Performance, Maintainability (17f9508)
- Authentication and authorization improvements

### Merged
- Merged local/nchantrs-ws branch into gamma (10327bb, 9e34fc6)

---

## [Unreleased] - v0.3.0

### Added
- AXN Upgrade Plan for systematic improvements
- Comprehensive TODO inventory (102 items documented)
- GlainMixin class for optional glain integration
- DataSourceDumper debug utilities for inspecting dialog data sources
- Verbose theme loading logs for debugging CSS issues

### Changed
- Force authentication always required (requires_auth = True)
- initView() now called in NchantdCape.__init__ to ensure proper initialization
- Theme configuration in YAML for flexibility

### Fixed
- Syntax error: nested double quotes in f-string
- syntax.py: Removed 4 duplicate class definitions (585 → 165 lines)
- syntax.py: Fixed FIXME triple-quote regex issues using raw strings
- Removed unused imports across multiple files
- Widget initialization timing issues
- Theme CSS: `#green` → `green` (invalid hex color name)
- logma.off() causing dialogs to not appear
- **P0-1.1**: Checkable attribute bug (PySide6 compatibility) in entries.py
- **P0-1.4**: Auth bypass - insecure default password + debug exception bypass in users.py

### Security
- Password dialog authentication added to NchantdCape
- **P0-1.4**: Fixed auth bypass vulnerabilities in users.py
  - Removed insecure default password generation (user.upper() + uuid)
  - Removed debug mode exception that exposed password hash

### Technical Debt
- Documentation rewritten (STATE.md, CHANGES.md, BREAKING_CHANGES.md)
- TODO comments organized into AXN plan
- Code audit: nchantdoffice reviewed as reference implementation

### Upgrade Scope
- **Scope**: nchantrs + nchantdoffice
- **Breaking changes**: OK if documented in BREAKING_CHANGES.md
- **Resolution**: Address in nchantdoffice (reference implementation)
- **Goal**: nchantrs becomes core codebase for Solutions Brewer products

---

## 2026-03-03 - v0.2.1

### Added
- Password dialog authentication to NchantdCape
- Detailed logging to NchantdCape.initView() flow
- Critical logging for debugging authentication issues

### Changed
- Force authentication always required (requires_auth = True)
- initView() now called in NchantdCape.__init__ to ensure proper initialization

### Fixed
- Syntax error: nested double quotes in f-string
- Removed unused imports across multiple files
- Widget initialization timing issues

---

## 2026-03-03 - v0.2.0

### Added
- GlainMixin class for optional glain integration
- init_glain_tables() method to NchantdStore
- get_glain_tables() method to NchantdStore
- Optional glain integration - no longer required

### Enhanced
- NchantdStore model with glain table support
- Graceful degradation when glain is not available
- Table prefix support for colocation

### Technical Details
- Chain: NchantdStore -> MicroStash -> SQuiRL
- Glain integration now optional via GlainMixin
- Tables use "glain_" prefix by default

---

## v0.1.x - Earlier Versions

See CHANGELOG.rst for historical changes.

## [0.3.0] - 2026-03-15

### Added
- pyright configuration for type checking
- mypy configuration for type checking
- isort configuration for import organization
- black configuration for code formatting
- flake8 configuration for linting
- Comprehensive test suite with 250+ test files
- Full module coverage for CLI commands
- Configuration file detection (nchantrs.yaml, config/nchantrs.yaml)
- CI/CD workflow configuration
- CONTRIBUTING.md guidelines
- CLI.md documentation

### Changed
- Updated CHANGES.md with comprehensive entries
- Improved documentation coverage
- Added type annotations to CLI module

### Fixed
- Fixed configuration file detection
- Fixed module import issues
- Added missing __main__.py entry point

## [0.2.9] - 2026-03-14

### Added
- Agent awareness support
- Package initialization with logging
- Version information

## [0.2.8] - 2026-03-13

### Added
- Initial gamma branch setup
- Comprehensive project structure
