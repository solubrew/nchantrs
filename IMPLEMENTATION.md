# Implementation Guide

## Entry Points & Backend Architecture

The nchantrs framework provides four entry points, each representing different levels of network complexity and backend configuration:

### Overview

| Entry Point | Backend | Primary Storage | Secondary Storage | Network |
|-------------|---------|-----------------|-------------------|---------|
| **aberration** | None | None | N/A | None |
| **distortion** | YAML/SQLite | YAML | SQLite | None |
| **nchantment** | SQLite+YAML | SQLite | YAML | None |
| **flection** | SQLite+YAML | SQLite | YAML | P2P (ZMQ) |

### Configuration Storage

Both **distortion** and **nchantment** support configurations existing outside of the SQLite database:

- **distortion** (YAML/SQLite): Primary YAML files, optional SQLite for runtime data
- **nchantment** (SQLite+YAML): Primary SQLite, with YAML config files outside the database

This allows flexibility in how applications store their configuration:

```
nchantdaxn/
├── config.yaml          ← YAML config (outside DB - distortion)
├── data.db              ← Optional SQLite
└── ...

# Or for nchantment:
nchantdoffice/
├── settings.db          ← SQLite (primary)
├── theme.yaml           ← YAML config (outside DB)
└── ...
```

### Choosing an Entry Point

| Use Case | Recommended Entry Point |
|----------|------------------------|
| No persistence needed | aberration |
| YAML-first, minimal SQLite | distortion |
| SQLite-first, YAML for external configs | nchantment |
| P2P networking required | flection |

## Internal Projects Dependencies

Per CODING_STANDARDS, internal projects (condor, ogma, nchantrs, pycurity) should **NOT** be included as dependencies in `pyproject.toml`. They must be:

- Installed separately in the environment
- Imported directly where needed
- Documented in STATE.md as runtime dependencies

### Why?

There is an issue with internal projects being registered incorrectly even on install when listed in pyproject.toml dependencies.
