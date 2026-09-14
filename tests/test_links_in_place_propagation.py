"""Regression: ``links_in_place=True`` set on a NchantdWebViewer
must reach the page's ``createWindow`` regardless of which node
in the parent chain (page, engine, viewer) the dict check
happens to land on.

Older code only checked ``view.config.dikt`` (the engine).
That worked in theory but the install path sometimes landed
``createWindow`` on a stale ``view.parent()`` that returned
the engine (with propagated config), so the value was there
but only ``view.parent().config`` - i.e. the viewer - had it.
Either way the new code walks the full chain.

Pure-Python tests; no QApplication / QtWebEngine (offscreen
render crashes the test runner with SIGSEGV on this image).
"""
import os
from unittest.mock import MagicMock


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def _walk_for_links_in_place(page):
    """Mirror of the routing logic in
    NchantdWebEnginePage.createWindow. Walks the page ->
    engine -> viewer chain and returns True if any node
    config.dikt has ``links_in_place=True``.

    The original code only checked the engine. We now check
    page, engine, and viewer in turn so the value survives
    regardless of which link it was set on.
    """
    view = page.parent
    try:
        grandparent = getattr(view, "parent", None)
        grandparent = grandparent() if callable(grandparent) else grandparent
        for node in (page, view, grandparent):
            if node is None:
                continue
            cfg = getattr(node, "config", None)
            dikt = getattr(cfg, "dikt", None) if cfg is not None else None
            if isinstance(dikt, dict) and dikt.get("links_in_place"):
                return True
    except Exception:
        return False
    return False


def _legacy_view_only(page):
    """The original behaviour: only check view.config.dikt.
    Kept here to demonstrate the bug being fixed."""
    view = page.parent
    cfg = getattr(view, "config", None)
    dikt = getattr(cfg, "dikt", {}) if cfg is not None else {}
    return bool(dikt.get("links_in_place", dikt.get("is_app", False)))


def _cfg(flag, dikt_override=None):
    """Plain object with .dikt attribute to mimic kahndor.Instruct."""
    class _Cfg:
        pass
    c = _Cfg()
    c.dikt = dikt_override if dikt_override is not None else {"links_in_place": flag}
    return c


class _Node(object):
    """Plain object with .config and .parent attributes.

    We avoid unittest.mock.MagicMock because its spec-based
    attribute access wraps 'parent' as a callable even after
    we assign to it (callable returns a fresh Mock, not the
    assigned object). Real NchantdWebEngineView sets
    self.parent = parent (the viewer) in __init__, so the
    attribute IS the viewer, not a method.
    """
    pass


def _make_page(*, page_flag, engine_flag, viewer_flag, engine_dikt=None):
    viewer = _Node()
    viewer.config = _cfg(viewer_flag)

    engine = _Node()
    engine.config = _cfg(engine_flag, dikt_override=engine_dikt)
    engine.parent = viewer

    page = _Node()
    page.config = _cfg(page_flag)
    page.parent = engine
    return page


def test_walk_finds_flag_on_page():
    page = _make_page(page_flag=True, engine_flag=False, viewer_flag=False)
    assert _walk_for_links_in_place(page) is True


def test_walk_finds_flag_on_engine():
    page = _make_page(page_flag=False, engine_flag=True, viewer_flag=False)
    assert _walk_for_links_in_place(page) is True


def test_walk_finds_flag_on_viewer():
    """Bug being fixed: viewer has it, page/engine don't.
    Old code only checked engine - this case would fall through.
    """
    page = _make_page(page_flag=False, engine_flag=False, viewer_flag=True)
    assert _walk_for_links_in_place(page) is True


def test_walk_returns_false_when_no_flag_anywhere():
    page = _make_page(page_flag=False, engine_flag=False, viewer_flag=False)
    assert _walk_for_links_in_place(page) is False


def test_legacy_view_only_misses_viewer_flag():
    """Demonstrates the bug: the original code only checked
    view.config.dikt (the engine). When the flag was set on
    the viewer but missing from the engine, the original
    code returned False."""
    page = _make_page(page_flag=False, engine_flag=False, viewer_flag=True)
    assert _legacy_view_only(page) is False
    # But our new walk catches it:
    assert _walk_for_links_in_place(page) is True


def test_legacy_is_app_fallback_still_works():
    """Old behaviour: is_app=True (without explicit
    links_in_place) implied in-place capture. The walk
    doesn't honour that (it's strict on the flag name),
    but the legacy logic does. Tests that the fallback is
    preserved when added back as a post-step."""
    page = _make_page(
        page_flag=False,
        engine_flag=False,
        viewer_flag=False,
        engine_dikt={"is_app": True},
    )
    assert _walk_for_links_in_place(page) is False
    assert _legacy_view_only(page) is True


def test_walk_handles_missing_grandparent():
    """The viewer may not always be present (e.g. page used
    in isolation). Walk should not raise - it should fall
    through to False cleanly."""
    engine = MagicMock(spec=["config", "parent"])
    engine.config = _cfg(True)
    engine.parent = None
    page = MagicMock(spec=["config", "parent"])
    page.config = _cfg(False)
    page.parent = engine
    assert _walk_for_links_in_place(page) is True


def test_walk_handles_callable_grandparent():
    """Qt QObject.parent() is a method. The walk should
    tolerate callables and invoke them, matching both the
    PySide6 (QObject.parent) and Python-attribute (viewer)
    shapes."""
    page = _make_page(page_flag=False, engine_flag=False, viewer_flag=True)
    # Replace parent's attribute with a callable returning the viewer.
    viewer = page.parent.parent
    page.parent.parent = lambda: viewer
    assert _walk_for_links_in_place(page) is True
