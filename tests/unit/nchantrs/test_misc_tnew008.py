"""Tests for T-NEW-008 fixes: media.py NEWSLArticle and help.py FAQ widget.

Uses AST + source-text assertions.
"""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MEDIA_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "media" / "media.py"
HELP_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "config" / "help.py"


@pytest.fixture(scope="module")
def media_source():
    return MEDIA_PATH.read_text()


@pytest.fixture(scope="module")
def media_ast(media_source):
    return ast.parse(media_source)


@pytest.fixture(scope="module")
def help_source():
    return HELP_PATH.read_text()


@pytest.fixture(scope="module")
def help_ast(help_source):
    return ast.parse(help_source)


def _find_class(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def _find_method(class_node, name):
    if class_node is None:
        return None
    for child in class_node.body:
        if isinstance(child, ast.FunctionDef) and child.name == name:
            return child
    return None


# ---------- NEWSLArticle (media.py) ----------

def test_newslarticle_class_exists(media_ast):
    """``NchantdNEWSLArticle`` should exist."""
    cls = _find_class(media_ast, "NchantdNEWSLArticle")
    assert cls is not None


def test_newslarticle_has_docstring(media_ast):
    """The class should have a docstring explaining the side-process pattern."""
    cls = _find_class(media_ast, "NchantdNEWSLArticle")
    docstring = ast.get_docstring(cls)
    assert docstring is not None
    assert "side process" in docstring.lower() or "cache" in docstring.lower()


def test_newslarticle_todo_removed(media_source, media_ast):
    """The stray TODO at the top of NchantdNEWSLArticle is removed."""
    cls = _find_class(media_ast, "NchantdNEWSLArticle")
    # The body should not contain the TODO
    for child in cls.body:
        if isinstance(child, ast.Expr) and isinstance(child.value, ast.Constant):
            if isinstance(child.value.value, str) and 'TODO' in child.value.value:
                pytest.fail(f'Class body contains a docstring TODO: {child.value.value}')


# ---------- HelpChatDex FAQ widget (help.py) ----------

def test_help_chat_dex_init_model_implements_faq_tree(help_ast):
    """``initModel`` should build a QTreeWidget for FAQs."""
    cls = _find_class(help_ast, "NchantdHelpChatDex")
    method = _find_method(cls, "initModel")
    assert method is not None
    body_src = ast.unparse(method)
    assert "QTreeWidget" in body_src, "initModel should build a QTreeWidget"
    assert "faq" in body_src.lower()


def test_help_chat_dex_init_model_has_docstring(help_ast):
    """``initModel`` should have a docstring explaining the FAQ tree."""
    cls = _find_class(help_ast, "NchantdHelpChatDex")
    method = _find_method(cls, "initModel")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "FAQ" in docstring or "Q/A" in docstring or "tree" in docstring.lower()


def test_help_chat_dex_init_model_pulls_from_store(help_ast):
    """``initModel`` should pull FAQs from the app store."""
    cls = _find_class(help_ast, "NchantdHelpChatDex")
    method = _find_method(cls, "initModel")
    body_src = ast.unparse(method)
    assert "store" in body_src.lower() or "get_faqs" in body_src


def test_help_chat_dex_init_model_handles_empty_faqs(help_ast):
    """``initModel`` should render a placeholder when the FAQ table is empty."""
    cls = _find_class(help_ast, "NchantdHelpChatDex")
    method = _find_method(cls, "initModel")
    body_src = ast.unparse(method)
    assert "placeholder" in body_src.lower() or "no faqs" in body_src.lower()


def test_help_chat_dex_init_model_handles_store_failure(help_ast):
    """``initModel`` should wrap the store call in try/except so a missing
    store doesn't crash the widget."""
    cls = _find_class(help_ast, "NchantdHelpChatDex")
    method = _find_method(cls, "initModel")
    body_src = ast.unparse(method)
    assert "try" in body_src
    assert "except" in body_src


def test_help_chat_dex_init_model_todo_removed(help_source, help_ast):
    """The stray TODO in ``initModel`` is removed."""
    cls = _find_class(help_ast, "NchantdHelpChatDex")
    method = _find_method(cls, "initModel")
    body_src = ast.unparse(method)
    assert "TODO build out a list of FAQs" not in body_src


def test_help_chat_dex_init_model_expands_tree(help_ast):
    """The FAQ tree should be expanded by default so all answers are visible."""
    cls = _find_class(help_ast, "NchantdHelpChatDex")
    method = _find_method(cls, "initModel")
    body_src = ast.unparse(method)
    assert "expandAll" in body_src
