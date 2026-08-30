"""T-NEW-162 part B (nchantrs side) — store_app_profile persists profile rows.

The 2026-08-18 PUSH-to-0.0.3 sweep filed T-NEW-162 part B covering
the cross-repo add_profile() storage path. The desktop side (T-NEW-162
part A) wires the cmd_add_profile handler with a has_pro gate that
delegates to ``self.add_profile``. The deferred add_profile body
references a non-existent ``self.profiles`` profile-manager; per the
DECIDE-1 matrix approved by the operator (2026-08-18), the storage
path goes through the nchantrs store's ``store_app_profile`` method.

Currently ``store_app_profile`` is a no-op stub
(``nchantrs/models/models.py:856``) that logs the call and returns
self — the desktop write goes through to the SQuiRL/MicroStash
pipeline but never lands a row. Tests pin a real implementation:

  1. ``store_app_profile`` calls ``self._store('app_profile', [record])``
     matching the sibling ``store_app_tab`` pattern at line 877.
  2. INSERT writes the row; UPDATE/DEACTIVATE/DELETE/ARCHIVE all
     route through the same ``_store`` helper with the appropriate
     ``how`` flag (rejected with the existing Exception pattern from
     line 853-855).
  3. Falls back to ``[]`` (or ``self``) when record is empty / db
     unavailable so callers don't crash on the bootstrap path.

Tests are AST-source structural + a minimal ``__new__`` smoke check
(mirroring the T-NEW-163 models.py pattern) because the nchantrs
NchantdStore subclasses MicroStash and SQLite connection setup is
not exercised in the headless test env.
"""

import ast
import inspect
from pathlib import Path

NCHANTRS_MODELS_PATH = (
    Path(__file__).parents[4]
    / "nchantrs/models/models.py"
)


def _function_source(name: str) -> str:
    tree = ast.parse(NCHANTRS_MODELS_PATH.read_text())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return ast.unparse(node)
    raise AssertionError(f"{name} not found")


def test_store_app_profile_is_no_longer_a_stub():
    """``store_app_profile`` body now calls ``self._store(...)``.

    The pre-fix body was just ``logma.info(...) ; return self`` —
    a no-op that silently swallowed the write. The T-NEW-162 part B
    fix lands a real ``_store('app_profile', [record])`` call.
    """
    source = _function_source("store_app_profile")
    assert "self._store" in source, (
        "store_app_profile must call self._store(...) to actually "
        "persist the row. Pre-fix body was a no-op stub "
        "(logma.info + return self)."
    )
    assert "'app_profile'" in source, (
        "store_app_profile must target the 'app_profile' table via "
        "self._store('app_profile', [record])."
    )


def test_store_app_profile_validates_how_parameter():
    """``store_app_profile`` rejects unknown ``how`` values.

    Mirrors the ``store_app_policy`` pattern at lines 853-855:
    raises ``Exception`` for any ``how`` not in the canonical set
    (``INSERT``, ``UPDATE``, ``DEACTIVATE``, ``DELETE``, ``ARCHIVE``).
    Pre-fix body had no validation — every ``how`` value silently
    landed at the no-op return-self branch.
    """
    source = _function_source("store_app_profile")
    assert "INSERT" in source and "UPDATE" in source, (
        "store_app_profile must validate 'how' against the canonical "
        "INSERT/UPDATE/DEACTIVATE/DELETE/ARCHIVE set, mirroring the "
        "store_app_policy pattern at nchantrs/models/models.py:853-855."
    )


def test_store_app_profile_signature_unchanged():
    """The public signature stays compatible with desktop callers.

    T-NEW-162 part A wires cmd_add_profile to call add_profile which
    in turn delegates to ``self.store.store_app_profile(record, db, how)``.
    The signature ``(self, record, db='db', how='INSERT')`` must
    stay byte-identical so desktop callers don't break.
    """
    import importlib

    # Use ast to confirm the signature, since importing the live
    # module pulls in SQLite / SQuiRL which isn't pytest-ready.
    tree = ast.parse(NCHANTRS_MODELS_PATH.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "store_app_profile":
            args = [a.arg for a in node.args.args]
            defaults = [
                ast.unparse(d) for d in (node.args.defaults or [])
            ]
            assert args == ["self", "record", "db", "how"], (
                f"store_app_profile arg names must stay "
                f"['self', 'record', 'db', 'how'], got {args}. "
                f"Desktop cmd_add_profile delegates through add_profile "
                f"to this signature."
            )
            assert defaults == ["'db'", "'INSERT'"], (
                f"store_app_profile defaults must stay ['db', 'INSERT'], "
                f"got {defaults}."
            )
            return
    raise AssertionError("store_app_profile not found in AST")


def test_get_app_profile_unchanged():
    """``get_app_profile`` signature stays compatible.

    T-NEW-162 part A wires get_profiles to delegate to
    ``self.app.model.get_profiles()`` which calls
    ``self.store.get_app_profile()["profile_txt"].values.tolist()``.
    The signature must stay compatible.
    """
    tree = ast.parse(NCHANTRS_MODELS_PATH.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "get_app_profile":
            args = [a.arg for a in node.args.args]
            assert "self" in args, "get_app_profile must keep self arg"
            assert "db" in args, "get_app_profile must keep db kwarg (used by desktop)"
            return
    raise AssertionError("get_app_profile not found")
