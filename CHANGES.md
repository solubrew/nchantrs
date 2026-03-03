# CHANGES.md - Nchantrs

All notable changes to the Nchantrs project will be documented in this file.

---

## [Unreleased] - v0.3.0

### Added
- AXN Upgrade Plan for systematic improvements
- Comprehensive TODO inventory (102 items documented)
- GlainMixin class for optional glain integration

### Changed
- Force authentication always required (requires_auth = True)
- initView() now called in NchantdCape.__init__ to ensure proper initialization
- Theme configuration in YAML for flexibility

### Fixed
- Syntax error: nested double quotes in f-string
- Removed unused imports across multiple files
- Widget initialization timing issues

### Security
- Password dialog authentication added to NchantdCape

### Technical Debt
- Documentation rewritten (STATE.md, CHANGES.md, BREAKING_CHANGES.md)
- TODO comments organized into AXN plan

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
