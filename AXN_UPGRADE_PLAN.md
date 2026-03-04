# Nchantrs Upgrade Plan - EXPANDED

## Overview
This plan organizes ALL issues found in the Nchantrs codebase into prioritized tasks for upgrades.

**Total Issues Found:** 110 (TODO: ~90, BUG: 1, HACK: 3, DEBUG: ~15)

---

## P0 - Critical Bugs (MUST FIX)

### Status: 🔴 In Progress

| ID | Location | Type | Description | Status |
|----|----------|------|-------------|--------|
| P0-01 | NchantdPyKey | BUG | initView() not executing - auth bypass | ⏳ Pending |
| P0-02 | widgets/media/editors/entries.py:96 | BUG | Checkable attribute bug in PySide6 | ⏳ Pending |
| P0-03 | utilities/users.py:233 | TODO | RSA key pair for encryption | ⏳ Pending |
| P0-04 | utilities/users.py:91 | TODO | Function call whitelist | ⏳ Pending |

---

## P1 - Authentication & Security

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P1-01 | utilities/users.py:106 | Password dialog implementation | ⏳ Pending |
| P1-02 | utilities/users.py:110 | Password rules implementation | ⏳ Pending |
| P1-03 | utilities/users.py:118 | User device details repull | ⏳ Pending |
| P1-04 | utilities/users.py:278 | Function whitelist enforcement (get_keys) | ⏳ Pending |
| P1-05 | utilities/users.py:293 | Function whitelist enforcement (get_secret) | ⏳ Pending |

---

## P2 - Database & Models

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P2-01 | models/applicationmodels.py:223 | Refactor get_current_node() | ⏳ Pending |
| P2-02 | models/applicationmodels.py:324 | Don't set new instance as active | ⏳ Pending |
| P2-03 | models/applicationmodels.py:372 | Method location evaluation | ⏳ Pending |
| P2-04 | models/applicationmodels.py:627 | Link table for link_affiliate | ⏳ Pending |
| P2-05 | models/treemodels.py:106 | Application startup optimization | ⏳ Pending |
| P2-06 | models/treemodels.py:384 | Connect to tabset model | ⏳ Pending |
| P2-07 | models/tabsetmodels.py:132 | Tabset getTabs fix | ⏳ Pending |
| P2-08 | models/tabsetmodels.py:137 | Tid identification | ⏳ Pending |
| P2-09 | models/tabsetmodels.py:139 | Tree-to-tabset connection | ⏳ Pending |
| P2-10 | models/tabsetmodels.py:170 | Active tab position storage | ⏳ Pending |
| P2-11 | models/tabsetmodels.py:190 | Get tabs for node | ⏳ Pending |
| P2-12 | models/tabsetmodels.py:212 | Tab position in widget | ⏳ Pending |
| P2-13 | models/tabsetmodels.py:242 | File path source refactor | ⏳ Pending |
| P2-14 | models/models.py:293 | Compress copy | ⏳ Pending |
| P2-15 | models/models.py:911 | Application configs integration | ⏳ Pending |
| P2-16 | models/models.py:1135 | Signal slot logic for crashed state | ⏳ Pending |
| P2-17 | models/models.py:1218 | Version config separation | ⏳ Pending |
| P2-18 | models/models.py:1405 | Edit name functionality | ⏳ Pending |

---

## P3 - Services

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P3-01 | services/upgrades.py:37 | Service/contract version check | ⏳ Pending |
| P3-02 | services/upgrades.py:101 | Stop web traffic (all) | ⏳ Pending |
| P3-03 | services/upgrades.py:104 | Stop web traffic (except servers) | ⏳ Pending |
| P3-04 | services/upgrades.py:107 | Stop background processes (ignore user) | ⏳ Pending |
| P3-05 | services/upgrades.py:110 | Stop background processes (respect user) | ⏳ Pending |
| P3-06 | services/upgrades.py:113 | Wait for low usage < 50% | ⏳ Pending |
| P3-07 | services/upgrades.py:116 | Wait for low usage < 25% | ⏳ Pending |
| P3-08 | services/license.py:35 | NFT contract finding | ⏳ Pending |

---

## P4 - Wizards

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P4-01 | wizards/apps.py:336 | Shortcut path fix | ⏳ Pending |
| P4-02 | wizards/apps.py:362 | Desktop file permissions | ⏳ Pending |
| P4-03 | wizards/apps.py:423 | Load primary instance | ⏳ Pending |
| P4-04 | wizards/apps.py:461 | App/Instance DB changes | ⏳ Pending |
| P4-05 | wizards/apps.py:506 | Pro version library controls | ⏳ Pending |
| P4-06 | wizards/users.py:211 | Pro level implementation | ⏳ Pending |
| P4-07 | nchantrs.py:86 | Wizard data connections | ⏳ Pending |

---

## P5 - UI/Widgets - Applications

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P5-01 | widgets/applications/applications.py:223 | DELTA level sync | ⏳ Pending |
| P5-02 | widgets/applications/applications.py:245 | initModel in separate process | ⏳ Pending |
| P5-03 | widgets/applications/applications.py:259 | Codec loading environment variables | ⏳ Pending |
| P5-04 | widgets/applications/applications.py:270 | Preload browser logic | ⏳ Pending |

---

## P6 - UI/Widgets - Browsers

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P6-01 | widgets/browsers/browsers.py:87 | PyfficeURLLibrary implementation | ⏳ Pending |
| P6-02 | widgets/browsers/browsers.py:125 | Browser to web app refactor | ⏳ Pending |
| P6-03 | widgets/browsers/browsers.py:226 | Multi-profile warning for pro users | ⏳ Pending |
| P6-04 | widgets/browsers/browsers.py:322 | Disable button handler | ⏳ Pending |
| P6-05 | widgets/browsers/browsers.py:598 | Web address tracking for redirects | ⏳ Pending |
| P6-06 | widgets/browsers/pages.py:777 | Download tracking | ⏳ Pending |
| P6-07 | widgets/browsers/pages.py:798 | Switch to MultiInstance | ⏳ Pending |

---

## P7 - UI/Widgets - Tabsets

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P7-01 | widgets/tabsets.py:340 | Close tag notes from previous tab | ⏳ Pending |
| P7-02 | widgets/tabsets.py:464 | Toolbox update timing | ⏳ Pending |
| P7-03 | widgets/tabsets.py:680 | Toolbox loading for active tab | ⏳ Pending |
| P7-04 | widgets/tabsets.py:683 | Open tag notes from current tab | ⏳ Pending |

---

## P8 - UI/Widgets - Calendars

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P8-01 | widgets/calendars/days.py:120 | Get tab name | ⏳ Pending |
| P8-02 | widgets/calendars/timelines.py:106 | Entries by time check/rotate | ⏳ Pending |
| P8-03 | widgets/calendars/timelines.py:245 | Today widget font size | ⏳ Pending |
| P8-04 | widgets/calendars/timelines.py:285 | NchantdTODOCalendar implementation | ⏳ Pending |
| P8-05 | widgets/calendars/timelines.py:307 | NchantdTODOEntryPane | ⏳ Pending |
| P8-06 | widgets/calendars/timelines.py:371 | TODO Action config | ⏳ Pending |

---

## P9 - UI/Widgets - Media

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P9-01 | widgets/media/images.py | Media image TODO items (3) | ⏳ Pending |
| P9-02 | widgets/media/editors/selectors.py | Media editor selectors (3) | ⏳ Pending |
| P9-03 | widgets/media/editors/editors.py | Media editors (1) | ⏳ Pending |
| P9-04 | widgets/media/media.py | Media base (2) | ⏳ Pending |

---

## P10 - UI/Widgets - Items

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P10-01 | widgets/items/nodes.py:255 | NchantdTreeNode accepting NchantdTreeItem | ⏳ Pending |
| P10-02 | widgets/items/nodes.py:440 | Theme pulling error | ⏳ Pending |
| P10-03 | widgets/items/nodes.py:529 | Batch update database positions | ⏳ Pending |
| P10-04 | widgets/items/catalogs.py:75 | Integrate super method for set_size | ⏳ Pending |
| P10-05 | widgets/items/catalogs.py:102 | Width heuristic | ⏳ Pending |

---

## P11 - UI/Widgets - Other

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P11-01 | widgets/tables/tables.py:487 | Split \n values for text length | ⏳ Pending |
| P11-02 | widgets/trees.py:129 | Error handling | ⏳ Pending |
| P11-03 | widgets/trees.py:390 | Read depth for flattening | ⏳ Pending |
| P11-04 | widgets/panes/catalogs.py:192 | Add tab.tid to NchantdDocumentCatalog | ⏳ Pending |
| P11-05 | widgets/panes/catalogs.py:229 | Dropdown for tab options | ⏳ Pending |
| P11-06 | widgets/panes/catalogs.py:248 | Rewrite left/right tab selection | ⏳ Pending |
| P11-07 | widgets/groups.py:431 | Scroll width HACK | ⏳ Pending |
| P11-08 | widgets/groups.py:432 | Horizontal scroll HACK | ⏳ Pending |
| P11-09 | widgets/groups.py:438 | Position calculation HACK | ⏳ Pending |
| P11-10 | widgets/forms/forms.py:103 | Max columns grid span | ⏳ Pending |
| P11-11 | widgets/forms/forms.py:195 | Load form data | ⏳ Pending |
| P11-12 | widgets/controls/connectors.py | Connectors (2) | ⏳ Pending |
| P11-13 | widgets/controls/buttons.py | Buttons (1) | ⏳ Pending |
| P11-14 | widgets/controls/button_groups.py | Button groups (1) | ⏳ Pending |
| P11-15 | widgets/catalogs.py:84 | Dynamic sizing | ⏳ Pending |
| P11-16 | widgets/agents/agents.py:95 | Sentinel status dialog | ⏳ Pending |

---

## P12 - Config & Dialogs

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P12-01 | widgets/config/settings.py | Settings (2) | ⏳ Pending |
| P12-02 | widgets/config/security.py | Security (1) | ⏳ Pending |
| P12-03 | widgets/config/uninstall.py | Uninstall (1) | ⏳ Pending |
| P12-04 | widgets/config/config.py | Config (1) | ⏳ Pending |
| P12-05 | dialogs/new.py:164 | Relocate validation | ⏳ Pending |
| P12-06 | dialogs/about.py:73 | List all add-on versions | ⏳ Pending |

---

## P13 - Utilities

### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P13-01 | utilities/comms.py:109 | Server running check | ⏳ Pending |
| P13-02 | utilities/debug.py | Debug utilities expansion | ⏳ Pending |

---

## Progress Tracker

| Priority | Total | Completed | In Progress | Pending |
|----------|-------|-----------|-------------|---------|
| P0 | 4 | 0 | 0 | 4 |
| P1 | 5 | 0 | 0 | 5 |
| P2 | 18 | 0 | 0 | 18 |
| P3 | 8 | 0 | 0 | 8 |
| P4 | 7 | 0 | 0 | 7 |
| P5 | 4 | 0 | 0 | 4 |
| P6 | 7 | 0 | 0 | 7 |
| P7 | 4 | 0 | 0 | 4 |
| P8 | 6 | 0 | 0 | 6 |
| P9 | 4 | 0 | 0 | 4 |
| P10 | 5 | 0 | 0 | 5 |
| P11 | 16 | 0 | 0 | 16 |
| P12 | 6 | 0 | 0 | 6 |
| P13 | 2 | 0 | 0 | 2 |
| **TOTAL** | **96** | **0** | **0** | **96** |

> Note: Some DEBUG comments excluded from count. Total ~110.

---

## Session Updates

### 2026-03-03

#### Completed This Session
- [x] P0: logma.off() fix (commit b5d5e92, 1931cf5)
- [x] P0: Theme CSS #green → green fix (commit c6bc679)
- [x] Added DataSourceDumper debug utilities
- [x] Added verbose theme loading logs
- [x] Audited nchantdoffice as reference implementation
- [x] Expanded AXN plan to 96 tasks across P0-P13
- [x] Updated CHANGES.md with session work
- [x] Defined upgrade scope: nchantrs + nchantdoffice

#### In Progress
- [ ] P0-02: Checkable attribute bug (entries.py:96)

#### Blocked
- [ ] Test machine needs reinstall to verify fixes

---

## Breaking Changes Log

See BREAKING_CHANGES.md for documented breaking changes.

---

## Entry Points (Preserved)
1. `nchantrs/nchantrs.py` - Main entry
2. `nchantrs/wizards/__init__.py` - Wizard launcher
3. `nchantrs/services/__init__.py` - Service runner
4. Test suite via `pytest`

---

## Goals
- **Speed**: Optimize tree/tabset operations
- **Stability**: Fix P0 bugs first
- **Maintainability**: Refactor get_current_node(), organize code
- **Security**: Implement RSA keys, password rules, whitelists
- **Compatibility**: PySide6 migration, UUID v7/v8

---

## Notes
- Scope: nchantrs + nchantdoffice
- Breaking changes: OK if documented in BREAKING_CHANGES.md
- Reference: NchantdOffice is the "source of truth" for fixes
- Internal projects: Use nchantrs.widgets.*, nchantrs.models.*, etc.
