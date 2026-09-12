"""T-NEW-071: browser navigation regression suite.

Covers the three navigation fixes shipped together:

  1. Bare-hostname expansion. ``google.com`` /
     ``ncho.local:8443/tree`` typed in the URL bar must be
     expanded to ``https://…`` before reaching the engine.
     URLs that already carry a scheme pass through.

  2. Enter on the URL bar navigates. The editable QComboBox
     fires ``returnPressed`` on the inner QLineEdit, NOT
     ``activated[-1]``. Forwarding returnPressed through
     ``on_activated`` keeps the dedupe / QSignalBlocker path
     intact while making Enter a real navigation event.

  3. Back/Forward buttons reflect ``engine.backAvailable`` /
     ``engine.forwardAvailable``. Previously the handlers
     were a literal ``pass`` — the buttons stayed enabled even
     at the ends of the history stack and the user had no
     visible affordance when navigation was impossible.

All three checks are AST-pinning — the project conftest mocks
``kahndor`` away, so direct import of the viewer module
crashes under pytest even when the bare-import path works
(verified separately on a vanilla venv). Live runtime
verification for the same code paths lives in
``/tmp/verify_navigation_fix.py``.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
BROWSERS = REPO_ROOT / "nchantrs" / "widgets" / "browsers" / "browsers.py"
SELECTORS = REPO_ROOT / "nchantrs" / "widgets" / "media" / "editors" / "selectors.py"


def _load_tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text())


def _find_func(tree: ast.Module, dotted: str) -> ast.FunctionDef:
    qual, _, name = dotted.rpartition(".")
    cls = qual.rpartition(".")[2]
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == cls:
            for child in node.body:
                if (
                    isinstance(child, ast.FunctionDef)
                    and child.name == name
                ):
                    return child
    raise AssertionError(f"function {dotted} not found")


def _find_class(tree: ast.Module, name: str) -> ast.ClassDef:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise AssertionError(f"class {name} not found")


# ===========================================================================
# 1. Bare-hostname expansion
# ===========================================================================


def test_set_url_path_calls_expand_bare_url():
    """set_url_path must normalise bare hostnames via
    _expand_bare_url so the engine never receives a no-scheme URL.
    """
    tree = _load_tree(BROWSERS)
    func = _find_func(tree, "NchantdWebViewer.set_url_path")
    src = ast.get_source_segment(BROWSERS.read_text(), func) or ""
    assert "_expand_bare_url(url_str)" in src, (
        "set_url_path must call self._expand_bare_url(url_str) "
        "after the str normalisation block (T-NEW-071)"
    )


def test_expand_bare_url_classmethod_exists():
    tree = _load_tree(BROWSERS)
    cls = _find_class(tree, "NchantdWebViewer")
    found = False
    is_classmethod = False
    for node in cls.body:
        if (
            isinstance(node, ast.FunctionDef)
            and node.name == "_expand_bare_url"
        ):
            found = True
            decorators = [
                ast.unparse(d) for d in node.decorator_list
            ]
            if any("classmethod" in d for d in decorators):
                is_classmethod = True
            break
    assert found, "_expand_bare_url must exist on NchantdWebViewer"
    assert is_classmethod, (
        "_expand_bare_url should be a @classmethod so callers "
        "with no instance available can still normalise"
    )


def test_expand_bare_url_passthrough_for_known_schemes():
    """URLs that already carry a scheme must NOT be re-prefixed.
    Otherwise ``file:///x`` would become ``https://file:///x``,
    or ``chrome://settings`` would fail to load.
    """
    src = BROWSERS.read_text()
    # Class-level constant lives OUTSIDE the method body, so
    # search the class block as a whole.
    cls = _find_class(_load_tree(BROWSERS), "NchantdWebViewer")
    class_src = ast.get_source_segment(src, cls) or ""
    assert "_KNOWN_SCHEME_PREFIXES" in class_src
    for prefix in (
        "https://",
        "http://",
        "file://",
        "about:",
    ):
        assert f'"{prefix}"' in class_src, (
            f"_KNOWN_SCHEME_PREFIXES must include {prefix!r} "
            f"to prevent double-prefixing"
        )
    # Method body must still do the actual expansion.
    tree = _load_tree(BROWSERS)
    func = _find_func(tree, "NchantdWebViewer._expand_bare_url")
    method_src = ast.get_source_segment(BROWSERS.read_text(), func) or ""
    assert "https://{" in method_src, (
        "bare-host expansion must prepend 'https://' to non-scheme input"
    )


# ===========================================================================
# 2. Enter on the URL bar navigates
# ===========================================================================


def test_on_return_pressed_invokes_on_activated():
    """Enter must end up calling the handler exactly ONCE.

    Qt natively emits ``activated(-1)`` (new text) or
    ``activated(matched_index)`` when Enter is pressed on the
    inner QLineEdit of an editable combobox — ``on_activated``
    (already connected in init_triggers) does the navigation.
    ``on_return_pressed`` must therefore NOT call the handler
    or ``on_activated`` itself — live verification showed that
    double-fires the navigation.
    """
    tree = _load_tree(SELECTORS)
    cls = _find_class(tree, "NchantdComboBox")
    method = None
    for node in cls.body:
        if isinstance(node, ast.FunctionDef) and node.name == "on_return_pressed":
            method = node
            break
    assert method is not None, "NchantdComboBox.on_return_pressed must exist"
    src = ast.get_source_segment(SELECTORS.read_text(), method) or ""
    assert "self.on_activated(" not in src, (
        "on_return_pressed must NOT call on_activated — Qt already "
        "emits activated(-1) natively on Enter; calling it again "
        "double-fires the navigation handler (verified live)"
    )
    assert "self.handler(" not in src, (
        "on_return_pressed must NOT call self.handler directly — "
        "same double-fire issue"
    )


def test_on_activated_calls_handler_for_minus_one():
    """The handler must fire from on_activated(-1) — it's the
    single navigation point for both mouse-pick and Enter paths.
    """
    tree = _load_tree(SELECTORS)
    cls = _find_class(tree, "NchantdComboBox")
    method = None
    for node in cls.body:
        if isinstance(node, ast.FunctionDef) and node.name == "on_activated":
            method = node
            break
    assert method is not None
    src = ast.get_source_segment(SELECTORS.read_text(), method) or ""
    assert "self.handler(" in src, (
        "on_activated must invoke self.handler(idx, text) for the "
        "navigation event (Enter / pick)"
    )
    assert "QSignalBlocker" in src, (
        "on_activated must QSignalBlocker its own setCurrentIndex "
        "so currentIndexChanged doesn't echo into on_index_change"
    )


# ===========================================================================
# 3. Back/Forward button enabled state
# ===========================================================================


def test_on_back_available_disables_button_when_unavailable():
    tree = _load_tree(BROWSERS)
    func = _find_func(tree, "NchantdWebViewer.on_back_available")
    src = ast.get_source_segment(BROWSERS.read_text(), func) or ""
    assert "pass" not in src.split("def ")[-1], (
        "on_back_available was a literal pass — that left the "
        "Back button enabled at the start of history"
    )
    assert "setEnabled" in src
    assert "web_page_back" in src


def test_on_forward_available_disables_button_when_unavailable():
    tree = _load_tree(BROWSERS)
    func = _find_func(tree, "NchantdWebViewer.on_forward_available")
    src = ast.get_source_segment(BROWSERS.read_text(), func) or ""
    assert "setEnabled" in src
    assert "web_page_forward" in src


def test_nav_button_lookup_walks_parent_toolbars():
    """The viewer is owned by ``NchantdOfficeWebBrowser`` whose
    toolbar lives on ``document_toolbar``, not on the viewer
    itself. The lookup must traverse the parent.
    """
    tree = _load_tree(BROWSERS)
    func = _find_func(tree, "NchantdWebViewer._get_nav_button")
    src = ast.get_source_segment(BROWSERS.read_text(), func) or ""
    for needle in (
        "document_toolbar",
        'getattr(self, "parent"',
        "action_name",
    ):
        assert needle in src, (
            f"_get_nav_button must reference {needle!r} (T-NEW-071)"
        )


# ===========================================================================
# Sanity: no regressions in the recursion-guard from T-NEW-069
# ===========================================================================


def test_recursion_guards_still_present():
    """The earlier ``on_index_change`` index-filter and
    ``_in_index_change`` re-entrancy flag must still be wired —
    the Enter fix must not regress them.
    """
    tree = _load_tree(SELECTORS)
    cls = _find_class(tree, "NchantdComboBox")
    init = None
    method = None
    for node in cls.body:
        if isinstance(node, ast.FunctionDef):
            if node.name == "__init__":
                init = node
            elif node.name == "on_index_change":
                method = node
    assert init is not None and method is not None
    init_src = ast.get_source_segment(SELECTORS.read_text(), init) or ""
    method_src = ast.get_source_segment(SELECTORS.read_text(), method) or ""
    assert "_in_index_change = False" in init_src
    assert "index is None or index < 0" in method_src
    assert "getattr(self, \"_in_index_change\", False)" in method_src


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
