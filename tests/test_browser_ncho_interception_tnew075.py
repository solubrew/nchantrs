# -*- coding: utf-8 -*-
"""T-NEW-075 (desk): ncho:// action interception on the Ad tab.

The slim-ad footer's "Get Pro" button uses the custom
``ncho://action/open_settings`` scheme. The desktop's WebEngine
has no built-in handler for that scheme, so the Ad tab swaps its
default ``QWebEnginePage`` for a subclass that:

  1. Sniffs ``url.scheme() == "ncho"`` in ``acceptNavigationRequest``.
  2. Dispatches to a registered Python callback.
  3. Returns ``False`` to swallow the navigation.

This file pins:

  - ``_NchoInterceptionPage`` exists in
    ``nchantdoffice.widgets.documents.atnrg.browsers``.
  - It subclasses ``NchantdWebEnginePage`` (so it inherits the
    stock logging + permission behaviour).
  - ``acceptNavigationRequest`` overrides the base.
  - The class accepts a ``handlers=`` dict.
  - ``NchantdOfficeAdTab.NCHO_ACTION_OPEN_SETTINGS`` is the
    constant the page snippet uses.
  - ``_install_ncho_interception_page`` swaps the engine's
    page for the interception subclass and wires the handler.
  - The handler map registers ``_open_settings_node``.
  - ``_open_settings_node`` delegates to
    ``app.view.switch_to_account_tab`` (falls back to
    ``app.switch_to_account_tab``).
  - ``initView`` calls the installer AFTER ``viewer.initWidget()``
    (so the viewer has already built its default page).

AST-level only — the offscreen PyQt fixture is not needed
because we don't load a real QWebEnginePage (which would need
a display and Chromium init). The behaviour of
``acceptNavigationRequest`` is unit-testable without QApplication
in principle, but the full Qt init dance is expensive and
orthogonal to what this PR changes.
"""
from __future__ import annotations

import ast
import os

AD_TAB_PATH = (
    "/home/solubrew/.hermes/projects/"
    "nchantdoffice/nchantdoffice/widgets/documents/atnrg/browsers.py"
)


def _load_ad_tab_ast():
    if not os.path.exists(AD_TAB_PATH):
        # Pytest skips cleanly if the sibling repo isn't checked
        # out — better than a hard import error.
        import pytest
        pytest.skip(f"{AD_TAB_PATH} not present")
    with open(AD_TAB_PATH) as fh:
        return ast.parse(fh.read())


def _find_classes(tree):
    return {n.name: n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}


def test_ncho_interception_page_class_exists():
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    assert "_NchoInterceptionPage" in classes, (
        "_NchoInterceptionPage missing — the Ad tab's "
        "ncho:// scheme interception won't work"
    )


def test_ncho_interception_page_subclasses_web_engine_page():
    """Must subclass NchantdWebEnginePage (not bare QWebEnginePage)
    so we inherit the existing navigation logging, permission
    handling, and ``navigationRequested`` signal behaviour.
    """
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    page = classes["_NchoInterceptionPage"]
    base_names = {b.id for b in page.bases if isinstance(b, ast.Name)}
    assert "NchantdWebEnginePage" in base_names, base_names


def test_ncho_interception_page_overrides_accept_navigation_request():
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    page = classes["_NchoInterceptionPage"]
    methods = {n.name for n in page.body if isinstance(n, ast.FunctionDef)}
    assert "acceptNavigationRequest" in methods, methods
    assert "__init__" in methods, methods


def test_ncho_interception_page_accepts_handlers_kwarg():
    """The constructor must accept ``handlers=...`` so the Ad
    tab can inject per-instance action callbacks."""
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    page = classes["_NchoInterceptionPage"]
    init = next(
        n for n in page.body
        if isinstance(n, ast.FunctionDef) and n.name == "__init__"
    )
    arg_names = {a.arg for a in init.args.args}
    assert "self" in arg_names
    # Either positional or keyword; we just need to know it
    # exists somewhere reachable. The kwonly path is the
    # canonical one for the Ad tab.
    all_args = list(init.args.posonlyargs) + list(init.args.args)
    kwonly = list(init.args.kwonlyargs)
    arg_names |= {a.arg for a in all_args}
    arg_names |= {a.arg for a in kwonly}
    arg_names |= {a.arg for a in init.args.kw_defaults if a is not None}
    assert "handlers" in arg_names, arg_names


def test_ad_tab_registers_open_settings_constant():
    """``NchantdOfficeAdTab.NCHO_ACTION_OPEN_SETTINGS`` must
    equal ``"ncho://action/open_settings"`` so the slim-ad
    footer href and the desktop handler map agree on the
    literal string.
    """
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    tab = classes["NchantdOfficeAdTab"]
    for node in tab.body:
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
            and node.targets[0].id == "NCHO_ACTION_OPEN_SETTINGS"
        ):
            assert ast.literal_eval(node.value) == "ncho://action/open_settings"
            return
    raise AssertionError("NCHO_ACTION_OPEN_SETTINGS constant missing")


def test_ad_tab_has_install_and_dispatch_methods():
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    tab = classes["NchantdOfficeAdTab"]
    methods = {n.name for n in tab.body if isinstance(n, ast.FunctionDef)}
    for m in ("_install_ncho_interception_page", "_open_settings_node"):
        assert m in methods, f"{m} missing from NchantdOfficeAdTab"


def test_init_view_calls_installer_after_viewer_initwidget():
    """The page swap must happen AFTER ``viewer.initWidget()`` —
    the installer depends on the default page already existing
    (it reads the engine's profile from it).
    """
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    tab = classes["NchantdOfficeAdTab"]
    init_view = next(
        n for n in tab.body
        if isinstance(n, ast.FunctionDef) and n.name == "initView"
    )
    # Walk every call node in order; the installer call must
    # come AFTER the initWidget call.
    calls = [
        c for c in ast.walk(init_view)
        if isinstance(c, ast.Call)
        and isinstance(c.func, ast.Attribute)
        and c.func.attr in ("initWidget", "_install_ncho_interception_page")
    ]
    # Walk in source order: ast.walk is pre-order which is
    # effectively source order for a function body. Compare the
    # positions of the two specific calls.
    pos = []
    for c in calls:
        if c.func.attr == "initWidget":
            pos.append(("initWidget", c.lineno))
        elif c.func.attr == "_install_ncho_interception_page":
            pos.append(("install", c.lineno))
    assert len(pos) == 2, pos
    assert pos[0][0] == "initWidget" and pos[1][0] == "install", pos
    assert pos[0][1] < pos[1][1], pos


def test_installer_wires_open_settings_handler():
    """The installer must register a handler for the
    ``ncho://action/open_settings`` action so clicks on the
    slim-ad footer's "Get Pro" button actually launch the
    Settings node.
    """
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    tab = classes["NchantdOfficeAdTab"]
    inst = next(
        n for n in tab.body
        if isinstance(n, ast.FunctionDef)
        and n.name == "_install_ncho_interception_page"
    )
    # The handler map is built as a dict literal; we walk the
    # AST for any reference to ``_open_settings_node`` and to
    # the constant.
    refs = "\n".join(ast.dump(n) for n in ast.walk(inst))
    assert "_open_settings_node" in refs, refs
    assert "NCHO_ACTION_OPEN_SETTINGS" in refs, refs


def test_open_settings_delegates_to_switch_to_account_tab():
    """The ``_open_settings_node`` handler must route through
    ``switch_to_account_tab`` — the canonical Settings-node
    launcher on the QMainWindow.
    """
    tree = _load_ad_tab_ast()
    classes = _find_classes(tree)
    tab = classes["NchantdOfficeAdTab"]
    opener = next(
        n for n in tab.body
        if isinstance(n, ast.FunctionDef) and n.name == "_open_settings_node"
    )
    refs = "\n".join(ast.dump(n) for n in ast.walk(opener))
    assert "switch_to_account_tab" in refs, refs
