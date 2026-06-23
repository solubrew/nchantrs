# Breaking Changes

This document tracks breaking changes in Nchantrs. Users should review this before upgrading.

---

## [Unreleased] - Future Release

### Planned Changes

#### API Renaming

- `NchantdApplication` → Deprecation planned, migrate to `NchantdCape` pattern
- Widget registration may change to decorator-based approach in v1.0

#### Configuration Schema

- YAML config schema version `1.x` will be deprecated in favor of `2.x`
- Required fields may be added/removed

#### Entry Point Changes

| Old Name | New Name | Notes |
|----------|----------|-------|
| `aberration` | TBD | May be merged into `distortion` |
| `distortion` | `YamlApp` | More descriptive naming |
| `nchantment` | `SqlApp` | Better reflects backend |
| `flection` | `P2PApp` | Network focus |

---

## [0.0.2.0] - Planned Next Release

### Changed

#### SQLite Backend
- **Database file naming**: Will use `.nchantrs.db` extension (currently `.db`)
- Migration tool will be provided

#### Theme System
- QSS template variables changed from `{{variable}}` to `@{variable}`
- Update your QSS templates before upgrading

#### Widget Registration
```python
# OLD (still supported but deprecated)
app.register_widget('my_widget.py')

# NEW (preferred from 0.0.2.0+)
app.register_widget_from_module('nchantrs.widgets.my_widget')
```

---

## [0.0.1.0] → [0.0.1.0.1]

### Breaking Changes

#### Module Renaming

| Old Module | New Module |
|------------|------------|
| `nchantrs.application` | `nchantrs.capes.distortion` |
| `nchantrs.models` | `nchantrs.cloaks` |
| `nchantrs.widgets` | `nchantrs.sigils` |

#### Import Changes

```python
# OLD imports (pre-0.0.1.0.1)
from nchantrs import NchantdApplication
from nchantrs.models import NchantdArticle

# NEW imports (0.0.1.0.1+)
from nchantrs.capes.distortion import NchantdDistortion
from nchantrs.cloaks.articles import NchantdArticle
```

#### Entry Point Changes

```python
# OLD
app = NchantdApplication(config)

# NEW
app = NchantdDistortion()
app.load_config('path/to/config.yaml')
```

#### Database Schema

- Table `nchantd_articles` renamed to `nchantd_items`
- Column `article_uuid` renamed to `item_uuid`
- Migration script provided in `migrations/` directory

#### Configuration YAML

```yaml
# OLD config format
app:
  name: MyApp
  type: distortion

# NEW config format (0.0.1.0.1+)
app_name: MyApp
entry_point: distortion
```

---

## Migration Guides

### Upgrading from pre-0.0.1.0.1 to 0.0.1.0.1+

1. **Update imports** in all Python files
2. **Run migration script**:
   ```bash
   python -m nchantrs.migrate --from=pre-0.0.1.0.1 --to=0.0.1.0.1
   ```
3. **Update YAML configs** to new format
4. **Test thoroughly** before production deployment

---

## Deprecation Timeline

| Feature | Deprecated In | Removed In |
|---------|---------------|------------|
| Old import paths | 0.0.1.0.1 | 0.1.0.0 |
| `{{variable}}` QSS syntax | 0.0.2.0 | 0.1.0.0 |
| `.db` file extension | 0.0.2.0 | 0.1.0.0 |
| Legacy widget registration | 0.0.2.0 | 1.0.0.0 |

---

*Last updated: 2026-06-22*
