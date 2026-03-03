# Nchantrs Upgrade Plan (AXN)

## 🎯 CURRENT FOCUS: Production Readiness

---

## 📋 Phase 1: Core Stability (Immediate)

### Authentication & Security
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🔴 P0 | Fix NchantdPyKey empty dialog bug | 🔴 OPEN | dialogs.py - initView() not executing |
| 🔴 P0 | Fix auth bypass in NchantdPyKeyWidget | 🔴 OPEN | _check_nchantrs_auth() skips auth |
| 🟡 P1 | Implement RSA key pair for encryption | 🔴 OPEN | utilities/users.py:233 |
| 🟡 P1 | Add password dialog standardization | 🔴 OPEN | utilities/users.py:106 |
| 🟡 P2 | Function call white-list for generators | 🔴 OPEN | utilities/users.py:91, 278, 293 |

### Critical Bugs
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🔴 P0 | Fix Checkable attribute bug | 🔴 OPEN | media/editors/entries.py:96 |
| 🟡 P1 | FIXMEs in syntax.py (triple-quotes) | 🔴 OPEN | libraries/syntax.py:71, 200, 364, 493 |
| 🟡 P2 | HACKs in groups.py scroll handling | 🔴 OPEN | widgets/groups.py:431-438 |

---

## 📋 Phase 2: Code Quality

### Refactoring
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🟡 P1 | Refactor node retrieval in models | 🔴 OPEN | models/applicationmodels.py:223 |
| 🟡 P1 | Refactor file_path handling | 🔴 OPEN | models/tabsetmodels.py:242 |
| 🟡 P2 | Move get_current_node logic to proper class | 🔴 OPEN | models/applicationmodels.py:372 |
| 🟢 P3 | Clean up TODO: integration needed | 🔴 OPEN | models/models.py:911 |

### Error Handling
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🟡 P1 | Add instance state crash handling | 🔴 OPEN | models/models.py:1135 |
| 🟡 P2 | Add tab position persistence | 🔴 OPEN | models/tabsetmodels.py:170 |

---

## 📋 Phase 3: Features & Enhancements

### Upgrades Service
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🟡 P1 | Connect to service/contract for version check | 🔴 OPEN | services/upgrades.py:37 |
| 🟡 P2 | Implement upgrade traffic controls | 🔴 OPEN | services/upgrades.py:101-116 |

### Wizards
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🟡 P1 | Fix shortcut path from app to install scripts | 🔴 OPEN | wizards/apps.py:336 |
| 🟡 P2 | Handle .desktop file permissions | 🔴 OPEN | wizards/apps.py:362 |
| 🟡 P2 | Implement primary instance loading | 🔴 OPEN | wizards/apps.py:423 |
| 🟢 P3 | Implement Pro-level library controls | 🔴 OPEN | wizards/apps.py:506 |

### Models
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🟡 P2 | Connect tree nodes to tabsets properly | 🔴 OPEN | models/tabsetmodels.py:132-139 |
| 🟡 P2 | Add link table for affiliate connections | 🔴 OPEN | models/applicationmodels.py:627 |
| 🟢 P3 | Fix pyffice_version reference | 🔴 OPEN | models/models.py:1218 |

### Widgets & Browsers
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🟡 P2 | Change browser to web app viewer | 🔴 OPEN | widgets/browsers/browsers.py:125 |
| 🟡 P2 | Add multi-profile user warning | 🔴 OPEN | widgets/browsers/browsers.py:226 |
| 🟡 P2 | Track web addresses for login redirects | 🔴 OPEN | widgets/browsers/browsers.py:598 |
| 🟢 P3 | Add download tracking | 🔴 OPEN | widgets/browsers/pages.py:777 |

### License & Pro Features
| Priority | Item | Status | Location |
|----------|------|--------|----------|
| 🟡 P2 | Find NFT contract connections | 🔴 OPEN | services/license.py:35 |
| 🟢 P3 | Implement Pro level features | 🔴 OPEN | wizards/users.py:211 |

---

## 📋 Phase 4: Technical Debt

### Documentation & Cleanup
| Priority | Item | Status |
|----------|------|--------|
| 🟢 P3 | Consolidate TODO comments into tickets |
| 🟢 P3 | Add docstrings to undocumented functions |
| 🟢 P3 | Remove dead code from models.py |

### Testing
| Priority | Item | Status |
|----------|------|--------|
| 🟡 P2 | Add unit tests for authentication flow |
| 🟡 P2 | Add integration tests for wizards |
| 🟢 P3 | Add tests for models CRUD operations |

---

## 📊 Summary Stats

| Category | Count |
|----------|-------|
| 🔴 P0 (Critical) | 3 |
| 🟡 P1 (High) | 18 |
| 🟡 P2 (Medium) | 15 |
| 🟢 P3 (Low) | 10 |
| **TOTAL** | **58** |

---

## 🔄 Related: NchantdPyKey Bug Context

### Symptom
Empty dialog appears, no password dialog shown

### Logs Show
1. Widget added to layout ✅
2. Widget displayed ✅
3. App exits 3 seconds later ❌
4. **Missing:** initView() called log
5. **Missing:** _show_password_dialog() log

### Root Cause
- `self.initView(cfg)` not being called in NchantdCape.__init__
- OR initView() crashes before logging
- Auth flow completely bypassed

### Next Steps
1. Add try/except around initView() call
2. Verify initView() executes
3. Debug why password dialog doesn't display
