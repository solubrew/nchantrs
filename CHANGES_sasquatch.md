# Sasquatch Auditor: Magic Numbers False Positives

## Problem

The `magic_numbers` dimension flags legitimate constants as "magic numbers" when they exceed 1000.

### Example False Positives

```python
# nchantrs/wizards/apps.py
REMOVE_PATH_FLAGS = 3213  # Flag for fonql.removePath()
fonql.removePath(path, REMOVE_PATH_FLAGS)

# nchantrs/models/nchantrs_models.py  
SETUP_RESET_FLAG = 3333  # Flag for setup reset
```

These are flagged because:
- They are integers > 1000
- They are NOT in `ACCEPTABLE_INT` set (0, 1, -1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 20, 24, 30, 60, 100, 200, 365, 500, 1000, 2000, 3600, 86400)

### Why These Are False Positives

1. **Already Constants**: `REMOVE_PATH_FLAGS` and `SETUP_RESET_FLAG` ARE named constants
2. **Not Magic**: The numbers are properly extracted to module-level constants with descriptive names
3. **Flag Values**: These are API/library flag values that MUST be these specific numbers

---

## Root Cause

The auditor's `_check_magic_numbers` method at line 5345 has flawed logic:

```python
# Find constant assignments (these "de-magic" the number)
constant_names = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if node.value and isinstance(node.value, (ast.Constant, ast.Num)):
                    constant_names.add(target.id)

# ...later...

# Only flag truly unusual numbers
if isinstance(value, int) and value not in ACCEPTABLE_INT:
    if value > 1000 or value < -1000:
        magic_numbers.append({...})  # FLAGS THE CONSTANT VALUE!
```

The problem: It finds the constant names BUT THEN doesn't use them to filter! It just checks if the raw numeric literal is > 1000.

---

## Fix Required

### 1. Use Constant Names to Filter Usage

When a numeric literal is found, check if it's being assigned to or read from a known constant name:

```python
# After finding constant_names, create a lookup
# If a number is being used via a constant reference (Name node), skip it
# Only flag if the number appears as a raw literal in function calls

# Example fix:
for node in ast.walk(tree):
    if isinstance(node, ast.Call):
        for arg in node.args:
            if isinstance(arg, ast.Constant) and isinstance(arg.value, (int, float)):
                # Check if this is a direct literal or via constant
                # If it's just a raw number like removePath(path, 3213) - flag it
                # If it's like removePath(path, REMOVE_PATH_FLAGS) - skip
```

### 2. Add Common Flag Values to Acceptable Set

Many libraries use flag integers > 1000:
- SQL flags (3213, 3333, etc.)
- API codes
- Protocol values
- Enum-like flags

```python
# Add to ACCEPTABLE_INT
ACCEPTABLE_INT = {0, 1, -1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 20, 24, 30, 60, 100, 200, 365, 500, 1000, 2000, 3600, 86400,
                  # Common flag values
                  3213, 3333, 4096, 8192, 16384, 32768, 65535, 65536}
```

### 3. Smart Detection: Check if Number is Used via Constant

The real fix: Track constant VALUE assignments, not just names:

```python
# Track constant VALUE -> name mappings
constant_values = {}  # {3213: "REMOVE_PATH_FLAGS"}
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if node.value and isinstance(node.value, (ast.Constant, ast.Num)):
                    if isinstance(node.value.value, int):
                        constant_values[node.value.value] = target.id

# When checking usage, see if value matches a constant
```

---

## Implementation Plan

### Option A: Quick Fix (Add Flag Values)
Add common flag values to ACCEPTABLE_INT - simple but incomplete.

### Option B: Proper Fix (Track Constant Values)
1. Parse all constant assignments with their values
2. When encountering a numeric literal, check if it's defined as a constant
3. Only flag if the number appears as a raw literal (not via constant reference)

### Recommended: Option C (Hybrid)
1. Add common flag ranges to acceptable set (3000-4000 for common flags)
2. Add logic to detect if number is being used via constant reference
3. Also check for patterns like `SomeEnum.VALUE` which are not magic

---

## Files to Modify

- `sasquatch/analysis/auditor.py` - `_check_magic_numbers` method (line 5345)

---

## Testing

After fix, these should pass:
```python
# These should NOT be flagged (already constants)
REMOVE_PATH_FLAGS = 3213
SETUP_RESET_FLAG = 3333

# These SHOULD still be flagged (truly magic)
def foo():
    return data[3213]  # Raw array index as magic number
```
