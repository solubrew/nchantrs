# Nchantrs Upgrade Plan

## Overview
This plan organizes 102 TODO items found in the Nchantrs codebase into prioritized tasks for upgrades.

---

## P0 - Critical (Must Fix)
### Status: ⏳ Pending

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P0-01 | NchantdPyKey | initView() not executing - auth bug | ⏳ Pending |
| P0-02 | media/editors/entries.py:96 | Checkable attribute bug | ⏳ Pending |
| P0-03 | syntax.py | FIXME: triple-quote issues | ⏳ Pending |

---

## P1 - High Priority

### Authentication & Security
| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P1-01 | utilities/users.py:106 | Password dialog implementation | ⏳ Pending |
| P1-02 | utilities/users.py:233 | RSA key pair for encryption | ⏳ Pending |
| P1-03 | utilities/users.py:91 | Function call whitelist | ⏳ Pending |
| P1-04 | utilities/users.py:110 | Password rules implementation | ⏳ Pending |

### Database & Models
| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P1-05 | models/applicationmodels.py:223 | Refactor get_current_node() | ⏳ Pending |
| P1-06 | models/applicationmodels.py:324 | Don't set new instance as active | ⏳ Pending |
| P1-07 | models/applicationmodels.py:627 | Link table for link_affiliate | ⏳ Pending |
| P1-08 | models/treemodels.py:106 | Application startup optimization | ⏳ Pending |

### Wizards
| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P1-09 | wizards/apps.py:336 | Shortcut path fix | ⏳ Pending |
| P1-10 | wizards/apps.py:423 | Load primary instance | ⏳ Pending |
| P1-11 | wizards/apps.py:461 | App/Instance DB changes | ⏳ Pending |
| P1-12 | nchantrs.py:86 | Wizard data connections | ⏳ Pending |

---

## P2 - Medium Priority

### Services
| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P2-01 | services/upgrades.py:37 | Service/contract version check | ⏳ Pending |
| P2-02 | services/upgrades.py:101-116 | Traffic control during upgrade | ⏳ Pending |
| P2-03 | services/license.py:35 | NFT contract finding | ⏳ Pending |

### UI/Widgets
| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P2-04 | models/treemodels.py:384 | Connect to tabset model | ⏳ Pending |
| P2-05 | models/tabsetmodels.py:132 | Tabset getTabs fix | ⏳ Pending |

### Utilities
| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P2-06 | utilities/comms.py:109 | Server running check | ⏳ Pending |
| P2-07 | utilities/users.py:278,293 | Function whitelist enforcement | ⏳ Pending |

---

## P3 - Low Priority

| ID | Location | Description | Status |
|----|----------|-------------|--------|
| P3-01 | wizards/apps.py:506 | Pro version library controls | ⏳ Pending |
| P3-02 | wizards/users.py:211 | Pro level implementation | ⏳ Pending |
| P3-03 | models/applicationmodels.py:372 | Method location evaluation | ⏳ Pending |

---

## Progress Tracker

| Priority | Total | Completed | In Progress | Pending |
|----------|-------|-----------|-------------|---------|
| P0 | 3 | 1 | 0 | 2 |
| P1 | 12 | 0 | 0 | 12 |
| P2 | 7 | 0 | 0 | 7 |
| P3 | 3 | 0 | 0 | 3 |
| **TOTAL** | **25** | **1** | **0** | **24** |

---

## 2026-03-03 Update

### Completed This Session
- [x] P0-01: logma.off() fix (commit b5d5e92, 1931cf5)
- [x] Theme CSS: #green → green fix (commit c6bc679)
- [x] Added DataSourceDumper debug utilities
- [x] Added verbose theme loading logs
- [x] Audited nchantdoffice as reference implementation
- [x] Updated CHANGES.md with session work
- [x] Defined upgrade scope: nchantrs + nchantdoffice

### In Progress
- [ ] P0-02: Checkable attribute bug (entries.py:96)
- [ ] Verify logma.off() fix on test machine

### Blocked
- Test machine needs reinstall to verify fixes

---

## Entry Points (Preserved)
1. `nchantrs.py` - Main entry
2. `wizards/__init__.py` - Wizard launcher
3. `services/__init__.py` - Service runner
4. Test suite via `pytest`

---

## Goals
- Speed: Optimize tree/tabset operations
- Stability: Fix P0 bugs first
- Maintainability: Refactor get_current_node(), organize code
- Security: Implement RSA keys, password rules, whitelists
