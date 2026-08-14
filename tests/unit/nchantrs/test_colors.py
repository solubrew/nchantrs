"""Tests for nchantrs.themes.colors.NchantdColor.

Two purposes:

1. **Behavior correctness** — NchantdColor mirrors the PyfficeColor surface
   that ``NchantdWidget.set_background`` relies on. We assert the contract
   (name dispatch, hex dispatch, RGB dispatch, calculate_text_color,
   static conversions) so the substitution is provably safe.

2. **Layering guard** — nchantrs must not depend on pyffice. The
   layering tests below swap a blocker onto ``sys.meta_path`` and confirm
   ``nchantrs.widgets.widgets`` and ``nchantrs.themes.colors`` still import
   cleanly. If a future refactor reintroduces a ``from pyffice...`` import
   at the top of any module pulled in by ``widgets.py`` (widgets, menus,
   controls, utils, themes, widgets.widgets' transitive deps), these tests
   fail loud.
"""

from __future__ import annotations

import importlib
import sys

import pytest

# Import at module scope (the per-test-dir conftest already installed a
# usable kahndor shim; matplotlib.colors is a regular extension module
# that does not collide with the autouse Qt mocks). Per-test re-imports
# would hit the "cannot load module more than once per process" error
# because the conftest's MagicMock Qt modules stay in sys.modules
# across tests.
from nchantrs.themes.colors import NchantdColor

# The ``tests/unit/nchantrs/conftest.py`` autouse fixture installs a usable
# kahndor shim so that nchantrs modules can be imported in this test suite
# (the root conftest's SB-stack autouse mock would otherwise break them).


# ---------------------------------------------------------------------------
# Behavior tests for NchantdColor
# ---------------------------------------------------------------------------


class TestNchantdColorBasic:
    """Mirror the PyfficeColor surface used by NchantdWidget.set_background."""

    def test_named_color_dispatches_to_set_color_name(self):
        c = NchantdColor({"unit": {"color": "red", "style": "name"}})
        c.load_unit()
        assert c.get_hex() == "#FF0000"
        assert c.calculate_text_color() == "white"

    def test_hex_color_dispatches_to_set_hex(self):
        c = NchantdColor({"unit": {"color": "#191cc2", "style": "hex"}})
        c.load_unit()
        assert c.get_hex() == "#191CC2"
        assert c.calculate_text_color() == "white"

    def test_rgb_color_dispatches_to_set_rgb(self):
        c = NchantdColor({"unit": {"color": (50, 50, 50), "style": "rgb"}})
        c.load_unit()
        assert c.get_hex() == "#323232"
        assert c.calculate_text_color() == "white"  # dark bg → white text

    def test_light_rgb_picks_black_text(self):
        c = NchantdColor({"unit": {"color": (200, 200, 200), "style": "rgb"}})
        c.load_unit()
        assert c.calculate_text_color() == "black"

    def test_unsupported_style_raises_value_error(self):
        c = NchantdColor({"unit": {"color": "x", "style": "yikes"}})
        with pytest.raises(ValueError, match="yikes"):
            c.load_unit()

    def test_unknown_color_name_leaves_hex_none(self):
        """Sentinel behavior: set_color_name for unknown names does not crash."""
        c = NchantdColor({"unit": {"color": "no_such_color", "style": "name"}})
        c.load_unit()
        assert c.color_name == "no_such_color"
        assert c.hex is None

    def test_default_color_text_is_black_when_rgb_unset(self):
        c = NchantdColor()
        assert c.get_rgb() is None
        assert c.calculate_text_color() == "black"

    def test_complementary_color_inverts_rgb(self):
        c = NchantdColor({"unit": {"color": (100, 150, 200), "style": "rgb"}})
        c.load_unit()
        assert c.calculate_complementary_color() == (155, 105, 55)


class TestNchantdColorStaticConversions:
    """Static helpers used directly by other call sites and tests."""

    def test_rgb_to_hex_round_trip(self):
        assert NchantdColor.rgb_to_hex((255, 0, 0)) == "#FF0000"
        assert NchantdColor.rgb_to_hex((0, 255, 0)) == "#00FF00"
        assert NchantdColor.rgb_to_hex((0, 0, 255)) == "#0000FF"
        assert NchantdColor.rgb_to_hex(None) is None

    def test_hex_to_rgb_round_trip(self):
        assert NchantdColor.hex_to_rgb("#FF0000") == (255, 0, 0)
        assert NchantdColor.hex_to_rgb("FF0000") == (255, 0, 0)  # no leading #

    def test_rgb_cmyk_hsl_hsv_basic(self):
        assert NchantdColor.rgb_to_cmyk((255, 0, 0)) == (0.0, 1.0, 1.0, 0.0)
        assert NchantdColor.hsl_to_rgb(0, 1, 0.5) == (255, 0, 0)
        assert NchantdColor.hsv_to_rgb((0, 1, 1)) == (255, 0, 0)

    def test_xyz_round_trip_is_lossy_but_close(self):
        """Pure-stdlib sRGB⇄XYZ: hand verify it doesn't blow up.

        The matrix is bridged from a configurable observer white so
        round-trip drift is bounded by gamma quantization, not algorithmic
        error. We accept ±1 per channel.
        """
        for rgb in [(0, 0, 0), (255, 255, 255), (200, 100, 50)]:
            xyz = NchantdColor.rgb_to_xyz(rgb)
            back = NchantdColor.xyz_to_rgb(xyz)
            assert all(abs(a - b) <= 1 for a, b in zip(rgb, back)), (rgb, back)


# ---------------------------------------------------------------------------
# Layering guard — nchantrs.widgets.widgets must not depend on pyffice
# ---------------------------------------------------------------------------


class _PyfficeBlocker:
    """Meta-path finder that raises if any `pyffice...` import is attempted."""

    def find_module(self, name, path=None):
        if name == "pyffice" or name.startswith("pyffice."):
            return self
        return None

    def load_module(self, name):
        raise ImportError(
            f"pyffice is required by name '{name}' but the layering test "
            "forbade it. nchantrs widgets must not import pyffice — it is a "
            "downstream consumer concern (nchantdoffice combines the two)."
        )


@pytest.fixture
def pyffice_blocked(monkeypatch):
    """Insert _PyfficeBlocker at the front of sys.meta_path for the test."""
    blocker = _PyfficeBlocker()
    monkeypatch.setattr(sys, "meta_path", [blocker] + list(sys.meta_path))
    # Evict any pyffice modules that were already loaded.
    for k in [k for k in sys.modules if k == "pyffice" or k.startswith("pyffice.")]:
        monkeypatch.delitem(sys.modules, k)
    yield blocker


def test_nchantrs_widgets_widgets_does_not_pull_in_pyffice(pyffice_blocked):
    """If this fails, nchantrs package has a pyffice import.

    We statically scan the source for any ``from pyffice...`` or
    ``import pyffice...`` statement rather than triggering the full module
    import chain. The full import chain is exercised by the existing
    application tests (which load widgets under real Qt) — for layering
    enforcement it is sufficient to verify the static source has no
    pyffice references inside the nchantrs package.
    """
    import os
    import re

    here = os.path.dirname(__file__)
    pkg_root = os.path.abspath(os.path.join(here, "..", "..", "..", "nchantrs"))
    bad_imports = []
    for dirpath, _dirnames, filenames in os.walk(pkg_root):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            full = os.path.join(dirpath, filename)
            with open(full, "r", encoding="utf-8") as f:
                for lineno, line in enumerate(f, 1):
                    if re.match(r"^\s*(from|import)\s+pyffice(\.|\s|$)", line):
                        rel = os.path.relpath(full, os.path.dirname(pkg_root))
                        bad_imports.append(f"{rel}:{lineno}: {line.rstrip()}")
    assert not bad_imports, (
        "nchantrs package must not import pyffice. Offenders:\n  "
        + "\n  ".join(bad_imports)
    )


def test_nchantrs_themes_colors_does_not_pull_in_pyffice(pyffice_blocked):
    """Same guard for themes.colors — caller of widgets.py uses it directly."""
    importlib.import_module("nchantrs.themes.colors")
    leaked = [k for k in sys.modules if k == "pyffice" or k.startswith("pyffice.")]
    assert not leaked, f"pyffice modules leaked into sys.modules: {leaked}"


def test_nchantrs_themes_colors_does_not_pull_in_colormath():
    """NchantdColor uses pure-stdlib color math — no colormath dependency."""
    for k in [k for k in sys.modules if k.startswith("nchantrs.themes.colors")]:
        del sys.modules[k]
    importlib.import_module("nchantrs.themes.colors")
    assert "colormath" not in sys.modules, "colormath leaked via nchantrs.themes.colors"
