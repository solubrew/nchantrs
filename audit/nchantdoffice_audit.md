# Nchantdoffice Audit Report

**Date:** 2026-03-03
**Auditor:** senbot

---

## Summary

| Aspect | Finding |
|--------|---------|
| **Project** | nchantdoffice (Todo application) |
| **Base Class** | NchantdCloak (multi-pane application) |
| **Files** | 11 Python files |
| **Status** | Functional but has TODOs |

---

## Key Patterns Observed

### 1. Model Layer
- `NTDAppModel` extends `NchantdCloakModel`
- `NTDTreeModel` extends `NchantdTreeModel`
- `NTDTabSetModel` extends `NchantdTabSetModel`
- Data stored in SQLite via nchantrs storage system

### 2. Widget Layer
- Heavy use of `NchantdEntryEditor` for text input
- Calendar widgets: `NchantdDateSelect`, `NchantdDateTimeGroup`, `NchantdMonthCalendar`
- Time tracking: `NchantdTimeTrackerForm`, `NchantdTimeTrackerFormFast`
- Tree widgets: `NchantdCustomTree`

### 3. Tab Structure
- TabSet-based navigation
- Dynamic tab generation from database
- Categories: Projects, Operations, Concerns, Resources, Tasks, Trackers

---

## TODOs Identified

### High Priority
| Location | Issue |
|----------|-------|
| `dstruct.py:94` | Tab setup uses name AND parent - needs consistency |
| `dstruct.py:97` | Should be base model function, not inline code |
| `dstruct.py:138` | UUID should upgrade to version 7 or 8 |

### Medium Priority
| Location | Issue |
|----------|-------|
| `dstruct.py:143` | Timeline node creation incomplete |
| `models.py:143` | Configuration integration from 2024-06-23 |

---

## Comparison: nchantdoffice vs nchantrs Main

| Feature | nchantdoffice | nchantrs |
|---------|---------------|----------|
| Base | NchantdCloak | NchantdCloak/NchantdCape |
| Files | 11 | 429 |
| Auth | Not implemented | NchantdPyKey |
| Theme | Uses nchantrs | Built-in |

---

## Recommendations

1. **Pull patterns from nchantdoffice** - It has working implementations of tree/tab navigation
2. **Fix TODOs** - The identified TODOs are straightforward fixes
3. **Consider merging** - nchantdoffice could be merged into nchantrs as example app
4. **Auth integration** - nchantdoffice doesn't have auth - good test case for nchantrs auth

---

## Next Steps

- [ ] Fix TODOs in dstruct.py
- [ ] Review UUID upgrade
- [ ] Test timeline node creation
- [ ] Consider merging nchantdoffice into nchantrs

---

*End of Audit*
