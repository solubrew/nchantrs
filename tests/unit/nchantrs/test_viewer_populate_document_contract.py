"""Regression — viewer.populate_document(url) is the AdTab navigation
contract (T-NEW-051 / T-NEW-069).

``NchantdOfficeAdTab._load_ad_layout`` invokes
``self.viewer.populate_document(url)`` on its inner
``NchantdWebViewer`` instance. The Viewer base class MUST expose
``populate_document`` — otherwise every layout switch / rotation
raises ``AttributeError`` silently and the ad tab goes blank.

History: the alias was originally only on ``NchantdWebBrowser``
(Browser subclass). The AdTab is a Document subclass that owns a
Viewer instance directly, so it bypassed the Browser subclass
entirely. Fix: hoist ``populate_document`` from Browser up to
Viewer.
"""
from __future__ import annotations
import pytest

qt = pytest.importorskip("PySide6")


def _bare_viewer(monkeypatch):
    """Construct an NchantdWebViewer with engine + url_select_entry
    stubbed. Skips initWidget's QApplication requirement by bypassing
    __init__ like other tests in this directory."""
    from nchantrs.widgets.browsers.browsers import NchantdWebViewer
    v = NchantdWebViewer.__new__(NchantdWebViewer)
    v._did_initial_load = False
    v.default_url = "http://default.invalid/"
    v.home_url = "http://default.invalid/"
    # Bare engine that records loads (no QApplication needed).
    class _Engine:
        def __init__(self):
            self.loads = []
        def load(self, url):
            self.loads.append(url)
    v.engine = _Engine()
    # url_select_entry is None for the AdTab shape (default_toolbar=False)
    v.url_select_entry = None
    v.config = type("Cfg", (), {"dikt": {"url_history": []}})()
    return v


def test_populate_document_exists_on_viewer_base():
    """The whole point of this regression: NchantdWebViewer (not
    just NchantdWebBrowser) must expose ``populate_document``.
    """
    from nchantrs.widgets.browsers.browsers import NchantdWebViewer
    assert hasattr(NchantdWebViewer, "populate_document")
    assert callable(getattr(NchantdWebViewer, "populate_document"))


def test_viewer_populate_document_loads_engine(monkeypatch):
    """AdTab contract: ``viewer.populate_document(url)`` calls
    ``engine.load(url)``. Before the fix this raised
    ``AttributeError`` and the tab went blank.
    """
    v = _bare_viewer(monkeypatch)
    url = "http://ads.slim/stack2?bucket=42"
    v.populate_document(url)
    # engine.load was called with the URL; rotation refreshes work.
    assert any("stack2" in str(u) for u in v.engine.loads)


def test_viewer_populate_document_accepts_nchantd_url(monkeypatch):
    """AdTab passes a ``NchantdURL`` object (not a string) — the
    alias must accept both forms and route through populate_viewport
    (which already unwraps NchantdURL to its string form).
    """
    from nchantrs.widgets.browsers.utilities import NchantdURL
    v = _bare_viewer(monkeypatch)
    # NchantdURL needs cfg= but takes a QUrl parent.
    cfg = {}
    url = NchantdURL("http://ads.slim/full?bucket=99", parent=v, cfg=cfg)
    v.populate_document(url)
    assert any("stack" in str(u) or "ads.slim" in str(u) for u in v.engine.loads)


def test_viewer_populate_document_none_is_safe(monkeypatch):
    """AdTab rotation can pass None during transient states — the
    alias must not crash (defensive, no-op is acceptable).
    """
    v = _bare_viewer(monkeypatch)
    # Should NOT raise.
    result = v.populate_document(None)
    assert result is v
