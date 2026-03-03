# BREAKING_CHANGES.md - Nchantrs

## 2026-03-03 - v0.2.1

### Authentication Required
**Impact: All applications using NchantdCape**

- NchantdCape now requires authentication by default
- Applications will show a password dialog before displaying content
- Set `requires_auth = False` in config to disable (not recommended for production)

### InitView Timing
**Impact: Custom widget initialization**

- `initView()` is now called in `NchantdCape.__init__` instead of after widget creation
- This ensures main_layout exists before widget operations
- Custom widgets should be compatible with this timing change

---

*No breaking changes in v0.2.0*
