# Nchantrs Upgrade Plan (AXN)

## 🎯 SCOPE: nchantrs + nchantdoffice

**Goal:** nchantrs becomes the core codebase for Solutions Brewer products.

---

## 📊 AUDIT COMPLETE

| Metric | Value |
|--------|-------|
| Total Python Files | 215 |
| Total Directories | 107 |
| TODO/FIXME/HACK/BUG | 110 |
| Files Audited | 100% |

---

## 🔴 PHASE 1: Critical Bugs (P0)

### Status: IN PROGRESS

| # | Issue | Location | Status |
|---|-------|----------|--------|
| 1.1 | Checkable attribute bug | widgets/media/editors/entries.py:96 | 🔴 OPEN |
| 1.2 | logma.off() dialog issue | dialogs/dialogs.py | ✅ FIXED |
| 1.3 | #green CSS error | themes/themes.py | ✅ FIXED |
| 1.4 | Auth bypass in NchantdPyKey | utilities/users.py | 🔴 OPEN |

---

## 🟡 PHASE 2: Code Quality (P1)

### 2.1 Libraries & Syntax
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 2.1.1 | FIXMEs in syntax.py | libraries/syntax.py:71, 200, 364, 493 | 🟡 IN PROGRESS |
| 2.1.2 | PyQt5 → PySide6 migration | libraries/*.py | 🔴 OPEN |
| 2.1.3 | UUID upgrade to v7/8 | dstruct.py | 🔴 OPEN |

### 2.2 Models
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 2.2.1 | Refactor node retrieval | models/applicationmodels.py:223 | 🔴 OPEN |
| 2.2.2 | Refactor file_path handling | models/tabsetmodels.py:242 | 🔴 OPEN |
| 2.2.3 | Instance state crash handling | models/models.py:1135 | 🔴 OPEN |

### 2.3 Utilities
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 2.3.1 | RSA key pair encryption | utilities/users.py:233 | 🔴 OPEN |
| 2.3.2 | Password dialog standardization | utilities/users.py:106 | 🔴 OPEN |
| 2.3.3 | Function call white-list | utilities/users.py:91, 278, 293 | 🔴 OPEN |

---

## 🟢 PHASE 3: Features & Enhancements (P2)

### 3.1 Services
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 3.1.1 | Version check service | services/upgrades.py:37 | 🔴 OPEN |
| 3.1.2 | Upgrade traffic controls | services/upgrades.py:101-116 | 🔴 OPEN |

### 3.2 Wizards
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 3.2.1 | App shortcut path | wizards/apps.py:336 | 🔴 OPEN |
| 3.2.2 | .desktop file permissions | wizards/apps.py:362 | 🔴 OPEN |
| 3.2.3 | Primary instance loading | wizards/apps.py:423 | 🔴 OPEN |

### 3.3 Widgets
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 3.3.1 | Browser to web app viewer | widgets/browsers/browsers.py:125 | 🔴 OPEN |
| 3.3.2 | Multi-profile user warning | widgets/browsers/browsers.py:226 | 🔴 OPEN |
| 3.3.3 | Login redirect tracking | widgets/browsers/browsers.py:598 | 🔴 OPEN |

---

## 🔵 PHASE 4: Technical Debt (P3)

### 4.1 Documentation
| # | Item | Status |
|---|------|--------|
| 4.1.1 | Consolidate TODOs into tickets | 🔴 OPEN |
| 4.1.2 | Add docstrings | 🔴 OPEN |
| 4.1.3 | Remove dead code | 🔴 OPEN |

### 4.2 Testing
| # | Item | Status |
|---|------|--------|
| 4.2.1 | Auth flow unit tests | 🔴 OPEN |
| 4.2.2 | Wizard integration tests | 🔴 OPEN |
| 4.2.3 | Model CRUD tests | 🔴 OPEN |

---

## 📈 PROGRESS TRACKING

### Completed This Session
- [x] Comprehensive codebase audit
- [x] File statistics analyzed
- [x] TODO/FIXME counts mapped
- [x] NchantdOffice patterns reviewed
- [x] Critical bugs identified
- [x] AXN task hierarchy created

### Remaining
- [ ] Push all audit docs to GitVein
- [ ] Start P0 bug fixes
- [ ] Update CHANGES.md with progress

---

## 🔗 REFERENCE: NchantdOffice

Working implementation patterns from nchantdoffice:
- Dynamic tree/tab generation from DB
- NchantdCloak base class inheritance
- Base64 content storage in `doc_media_content.content_enc64_txt`

---

## 📝 Breaking Changes Policy

- Breaking changes are **OK**
- Must be documented in BREAKING_CHANGES.md
- Resolution required in nchantdoffice (reference impl)

---

*Last Updated: 2026-03-03*
*Status: AUDIT COMPLETE - Ready for P0 fixes*
