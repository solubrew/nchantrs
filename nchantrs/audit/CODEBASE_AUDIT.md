# Nchantrs Comprehensive Codebase Audit

## 📊 Overview

| Metric | Value |
|--------|-------|
| **Total Python Files** | 215 |
| **Total Directories** | 107 |
| **TODO/FIXME/HACK/BUG Count** | 110 |
| **Scope** | nchantrs + nchantdoffice |
| **Status** | Audit In Progress |

---

## 🗂️ Module Structure

### Core Application Modules

| Module | Files | Key Files | Status |
|--------|-------|-----------|--------|
| **actions** | 8 | actions.py, tables.py, tree.py | ✅ Stable |
| **dialogs** | 12 | dialogs.py (~728 lines) | 🔧 Needs Fix |
| **events** | 6 | events.py, keyboard_events.py, mouse_events.py | ✅ Stable |
| **extensions** | 7 | apis.py, plugins.py | 🟡 In Dev |
| **libraries** | 4 | syntax.py | 🔧 Needs Fix |
| **models** | 4 | models.py (~1901 lines), applicationmodels.py | 🔧 Needs Fix |
| **services** | 11 | upgrades.py, integrity.py | 🟡 In Dev |
| **themes** | 3 | themes.py | 🔧 Needs Fix |
| **utilities** | 15 | users.py, debug.py, comms.py | 🟡 In Dev |
| **views** | 4 | applicationviews.py, treeviews.py | ✅ Stable |
| **widgets** | 50+ | widgets.py (~1011 lines), applications.py (~30k) | 🔧 Needs Fix |
| **wizards** | 7 | apps.py (~26k), users.py | 🟡 In Dev |

### Widget Submodules

| Submodule | Status | Notes |
|-----------|--------|-------|
| **widgets/applications** | ✅ Working | NchantdCloak base class |
| **widgets/browsers** | 🟡 In Dev | 13 files, full browser engine |
| **widgets/calendars** | ✅ Stable | Timelines, calendars |
| **widgets/media** | 🔧 Needs Fix | Editors have checkable bug |
| **widgets/tables** | ✅ Stable | Table widgets |
| **widgets/tabsets** | 🔧 Needs Fix | Tab management |
| **widgets/trees** | ✅ Stable | Tree widgets |
| **widgets/items** | ✅ Stable | Node and catalog items |
| **widgets/panes** | ✅ Stable | Panes and catalogs |
| **widgets/controls** | ✅ Stable | Form controls |
| **widgets/forms** | ✅ Stable | Form widgets |

---

## 🔴 Critical Issues (P0)

| Issue | Location | Description |
|-------|----------|-------------|
| Checkable attribute bug | widgets/media/editors/entries.py:96 | PySide6 compatibility |
| logma.off() dialog issue | dialogs/dialogs.py | Dialogs not showing |
| #green CSS error | themes/themes.py | Color parsing error |

---

## 🟡 High Priority (P1)

| Issue | Location | Description |
|-------|----------|-------------|
| FIXMEs in syntax.py | libraries/syntax.py:71, 200, 364, 493 | Triple-quote issues |
| Auth bypass | utilities/users.py | _check_nchantrs_auth() |
| UUID upgrade needed | dstruct.py | Upgrade to v7/8 |

---

## 📁 File Statistics (Top 20 by Size)

| File | Lines | Purpose |
|------|-------|---------|
| widgets/applications/ap30k | Main application class |
| wizards/apps.py |plications.py | ~ ~26k | Application wizard |
| widgets/browsers/browsers.py | ~23k | Browser widget |
| widgets/browsers/pages.py | ~38k | Browser pages |
| widgets/browsers/profiles.py | ~31k | Browser profiles |
| widgets/browsers/downloads.py | ~29k | Download manager |
| models/models.py | ~1901 | Core models |
| widgets/widgets.py | ~1011 | Base widget class |
| dialogs/dialogs.py | ~728 | Dialog system |
| libraries/syntax.py | ~6.6k | Syntax highlighting |

---

## 🔄 Reference: NchantdOffice Patterns

NchantdOffice demonstrates working implementations:

1. **Tree/Tab Generation** - Dynamic generation from database
2. **NchantdCloak Inheritance** - Proper base class usage
3. **Base64 Content Handling** - Content stored encoded in `doc_media_content.content_enc64_txt`

---

## 📋 Audit Checklist

- [x] Core modules cataloged
- [x] Widget submodules cataloged
- [x] File sizes analyzed
- [x] TODO/FIXME counts mapped
- [x] Critical issues identified
- [x] NchantdOffice patterns reviewed
- [ ] AXN task hierarchy created
- [ ] Priority ordering confirmed
- [ ] Breaking changes documented

---

## Next Steps

1. Create detailed AXN task hierarchy
2. Prioritize fixes by dependency order
3. Start with P0 critical bugs
4. Document any breaking changes in BREAKING_CHANGES.md
