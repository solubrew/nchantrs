# CHANGES.md - Nchantrs

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
