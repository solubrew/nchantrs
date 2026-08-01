"""Per-test-dir conftest for tests/unit/nchantrs/.

The root ``tests/conftest.py`` installs an autouse fixture that mocks
``kahndor``, ``squirl``, ``subtrix``, ``pycurity``, ``micromole`` with
``MagicMock`` at test time. ``MagicMock`` is not a real package, so any
nested attribute access like ``kahndor.logma`` or code that does
``kahndor.Instruct(pxcfg).select(...).dikt.get(...)`` fails silently
(returning MagicMock values) and tests that exercise nchantrs models
that depend on real kahndor config behavior break.

This conftest overrides the autouse SB-stack mock for the colors test
suite by providing a real ``kahndor`` module shim that:
- exposes ``kahndor.Instruct`` as a thin wrapper that stores the dict
  in ``.dikt`` and returns itself from ``.select()`` / ``.override()``
- exposes ``kahndor.logma.Logma`` as a no-op
- leaves ``squirl``, ``subtrix``, ``pycurity``, ``micromole`` stubs
  available for the wider test suite

The blocker is installed by the ``real_kahndor`` autouse fixture, which
runs *before* the root conftest's autouse ``mock_external_dependencies``
because it is declared in a more-specific conftest path.
"""

from __future__ import annotations

import sys
import types
from unittest.mock import MagicMock

import pytest


class _DummyInstruct:
    """Lightweight kahndor.Instruct replacement for tests.

    Behaves like the parts of kahndor.Instruct that nchantrs uses:
        config = kahndor.Instruct(pxcfg)            # wrap dict
        config = config.select("SectionName")        # no-op
        config = config.override(cfg)                # merge dict
        config.dikt.get("key", default)              # dict lookup
    """

    def __init__(self, dikt=None):
        self.dikt = dict(dikt) if isinstance(dikt, dict) else {}

    def select(self, _name):
        return self

    def override(self, cfg):
        if cfg is None:
            return self
        if isinstance(cfg, _DummyInstruct):
            self.dikt.update(cfg.dikt)
        elif isinstance(cfg, dict):
            self.dikt.update(cfg)
        return self


def _install_real_kahndor():
    """Replace the conftest's MagicMock kahndor with a usable shim."""
    kahndor = types.ModuleType("kahndor")
    kahndor.Instruct = _DummyInstruct
    kahndor_logma = types.ModuleType("kahndor.logma")

    class _DummyLogma:
        def __init__(self, *_args, **_kwargs):
            pass

        def off(self):
            return None

        def info(self, *_args, **_kwargs):
            return None

        def debug(self, *_args, **_kwargs):
            return None

        def warning(self, *_args, **_kwargs):
            return None

        def error(self, *_args, **_kwargs):
            return None

    kahndor_logma.Logma = _DummyLogma
    sys.modules["kahndor"] = kahndor
    sys.modules["kahndor.kahndor"] = kahndor
    sys.modules["kahndor.logma"] = kahndor_logma

    # kahndor.utils.thingify is needed by some nchantrs modules
    kahndor_utils = types.ModuleType("kahndor.utils")
    kahndor_utils.thingify = MagicMock()
    sys.modules["kahndor.utils"] = kahndor_utils


@pytest.fixture(autouse=True)
def real_kahndor(monkeypatch):
    """Install a usable kahndor shim so nchantrs modules can be imported."""
    prior = {k: sys.modules.get(k) for k in ("kahndor", "kahndor.kahndor", "kahndor.logma", "kahndor.utils")}
    _install_real_kahndor()
    yield
    for k, v in prior.items():
        if v is None:
            sys.modules.pop(k, None)
        else:
            sys.modules[k] = v
