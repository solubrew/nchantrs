"""Regression coverage for link-filter construction."""

from pathlib import Path
import ast


def test_get_links_uses_existing_where_clause_builder():
    """get_links must not call the removed _build_filter_config helper."""
    source = Path("nchantrs/models/models.py").read_text()
    tree = ast.parse(source)
    store = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "NchantdStore")
    method = next(node for node in store.body if isinstance(node, ast.FunctionDef) and node.name == "get_links")
    body = ast.unparse(method)

    assert "self._build_where_clause" in body
    assert "self._build_filter_config" not in body
