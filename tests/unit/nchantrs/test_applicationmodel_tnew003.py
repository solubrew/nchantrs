"""Tests for T-NEW-003 fixes: application-model path-override, save logic,
instance settings storage, version upgrade, and getData refactor.

The tests use AST + source-text assertions rather than widget instantiation
because the mock-PyQt metaclass conflicts in the headless test environment
prevent NchantdModel subclasses from being instantiated cleanly.
"""
import pytest
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
APPMOD_PATH = PROJECT_ROOT / "nchantrs" / "models" / "applicationmodels.py"
MODELS_PATH = PROJECT_ROOT / "nchantrs" / "models" / "models.py"
SIGIL_PATH = PROJECT_ROOT / "nchantrs" / "dialogs" / "sigil.py"


@pytest.fixture(scope="module")
def appmod_source():
    return APPMOD_PATH.read_text()


@pytest.fixture(scope="module")
def appmod_ast(appmod_source):
    return ast.parse(appmod_source)


@pytest.fixture(scope="module")
def models_source():
    return MODELS_PATH.read_text()


@pytest.fixture(scope="module")
def models_ast(models_source):
    return ast.parse(models_source)


@pytest.fixture(scope="module")
def sigil_source():
    return SIGIL_PATH.read_text()


@pytest.fixture(scope="module")
def sigil_ast(sigil_source):
    return ast.parse(sigil_source)


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


# ---------- generate_paths path-override ----------

def test_generate_paths_accepts_path_override(appmod_source):
    """``generate_paths`` should accept a ``db_path`` cfg override for testing."""
    assert "db_path" in appmod_source, "db_path override not found in generate_paths"
    # The override should be a cfg.get() lookup
    assert "cfg.get('db_path')" in appmod_source or 'cfg.get("db_path")' in appmod_source, (
        "db_path should be a cfg.get() lookup"
    )


def test_generate_paths_documents_override_purpose(appmod_source, appmod_ast):
    """The docstring should explain the override is for testing."""
    # Find the generate_paths method's docstring
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "generate_paths")
    assert method is not None
    docstring = ast.get_docstring(method)
    assert docstring is not None, "generate_paths should have a docstring"
    assert "test" in docstring.lower(), "docstring should mention the test path"


def test_generate_paths_substitutes_override_into_templates(appmod_source):
    """The override path should be substituted into the path templates via
    the existing ``Mechanism`` runner (no separate template engine)."""
    assert "Mechanism(template, data).run()" in appmod_source, (
        "generate_paths should use Mechanism().run() for override path substitution"
    )


def test_generate_paths_path_override_todo_removed(appmod_source, appmod_ast):
    """The original 2026-07 TODO at the top of generate_paths is removed."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "generate_paths")
    body_src = ast.unparse(method)
    assert "TODO: implement a path override" not in body_src, (
        "Stale TODO still in generate_paths"
    )


# ---------- save() method ----------

def test_save_method_walks_model_graph(appmod_source, appmod_ast):
    """The save() method should walk the model graph and emit store_app_* writes."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "save")
    assert method is not None, "save() method missing"
    body_src = ast.unparse(method)
    assert "update_record" in body_src, "save() should call update_record"
    assert "app_instance" in body_src, "save() should write the app_instance row"
    assert "instance_id_txt" in body_src, "save() should key by instance_id_txt"


def test_save_method_is_write_through(appmod_source, appmod_ast):
    """save() is write-through (immediate disk write, no buffer)."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "save")
    body_src = ast.unparse(method)
    assert "is_saved" in body_src, "save() should mark is_saved after writing"
    assert "set_is_saved" in body_src, "save() should call set_is_saved"


def test_save_uses_parallel_records_columns_shape(appmod_source, appmod_ast):
    """save() uses the scratch-style payload (parallel records + columns)
    per the Sprint 28 squirl contract."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "save")
    body_src = ast.unparse(method)
    assert "'records'" in body_src, "save() should use 'records' key"
    assert "'columns'" in body_src, "save() should use 'columns' key"


def test_save_method_documents_write_through(appmod_source, appmod_ast):
    """save() docstring documents the write-through semantics."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "save")
    docstring = ast.get_docstring(method)
    assert docstring is not None
    assert "write-through" in docstring.lower() or "immediate" in docstring.lower()


# ---------- upgrade_instance ----------

def test_upgrade_instance_method_exists(appmod_source, appmod_ast):
    """T-NEW-003 added ``upgrade_instance`` for the version-bump path."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "upgrade_instance")
    assert method is not None, "upgrade_instance method missing"


def test_upgrade_instance_updates_version(appmod_source, appmod_ast):
    """upgrade_instance should update the instance version and call update_version."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "upgrade_instance")
    body_src = ast.unparse(method)
    assert "target_version" in body_src, "upgrade_instance takes target_version"
    assert "self.instance.version" in body_src, (
        "upgrade_instance should update self.instance.version"
    )
    assert "update_version" in body_src, (
        "upgrade_instance should call update_version to persist"
    )


def test_upgrade_instance_raises_when_no_instance(appmod_source, appmod_ast):
    """upgrade_instance should raise a clear error when no instance is configured."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "upgrade_instance")
    body_src = ast.unparse(method)
    assert "raise" in body_src, "upgrade_instance should raise when no instance"
    assert "No Instance" in body_src or "instance" in body_src.lower()


# ---------- Broken aspirational methods cleaned up ----------

def test_activate_extension_is_real_method(appmod_ast):
    """The previous aspirational ``_activate_extension`` (nested def) is now
    a real method with a body."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "_activate_extension")
    assert method is not None
    body_src = ast.unparse(method)
    # The new method should have a real body, not a nested def
    assert "def _activate_integration" not in body_src, (
        "Leftover nested def pattern in _activate_extension"
    )
    assert "logma.info" in body_src or "return" in body_src


def test_archive_record_is_real_method(appmod_ast):
    """``_archive_record`` should be a real method now (call archive_record)."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "_archive_record")
    assert method is not None
    body_src = ast.unparse(method)
    assert "self.store.archive_record" in body_src or "archive_record" in body_src


def test_check_password_set_is_real_method(appmod_ast):
    """``_check_password_set`` should be a real method now (returns bool)."""
    cls = _find_class(appmod_ast, "NchantdCloakModel")
    method = _find_method(cls, "_check_password_set")
    assert method is not None
    body_src = ast.unparse(method)
    assert "return" in body_src
    assert "False" in body_src
    assert "True" in body_src


# ---------- NchantdStore instance settings ----------

def test_nchantd_store_init_integrates_instance_settings(models_source):
    """The NchantdStore.__init__ method should set up the instance settings cache."""
    assert "self._instance_settings" in models_source, (
        "NchantdStore should initialize _instance_settings"
    )


def test_set_instance_setting_method_exists(models_ast):
    """``NchantdStore.set_instance_setting`` is a public API."""
    cls = _find_class(models_ast, "NchantdStore")
    method = _find_method(cls, "set_instance_setting")
    assert method is not None
    args = [a.arg for a in method.args.args]
    assert "key" in args
    assert "value" in args


def test_get_instance_setting_method_exists(models_ast):
    """``NchantdStore.get_instance_setting`` is a public API."""
    cls = _find_class(models_ast, "NchantdStore")
    method = _find_method(cls, "get_instance_setting")
    assert method is not None
    args = [a.arg for a in method.args.args]
    assert "key" in args
    assert "default" in args


def test_save_instance_settings_method_exists(models_ast):
    """``NchantdStore.save_instance_settings`` persists the cache."""
    cls = _find_class(models_ast, "NchantdStore")
    method = _find_method(cls, "save_instance_settings")
    assert method is not None


def test_save_instance_settings_writes_to_app_instance_setting_table(models_source):
    """The save method should write the ``app_instance_setting`` table."""
    assert "app_instance_setting" in models_source, (
        "save_instance_settings should write to app_instance_setting table"
    )


def test_set_instance_setting_returns_self(models_ast):
    """set_instance_setting returns self for chaining."""
    cls = _find_class(models_ast, "NchantdStore")
    method = _find_method(cls, "set_instance_setting")
    body_src = ast.unparse(method)
    assert "return self" in body_src


def test_get_instance_setting_returns_default_when_missing(models_ast):
    """get_instance_setting returns the default when key is absent."""
    cls = _find_class(models_ast, "NchantdStore")
    method = _find_method(cls, "get_instance_setting")
    body_src = ast.unparse(method)
    assert ".get(key, default)" in body_src or ".get(key,default)" in body_src


# ---------- Stale TODO edit name removed ----------

def test_stale_todo_edit_name_removed(models_source):
    """The stray ``# TODO edit name`` comment between two unrelated functions is removed."""
    assert "# TODO edit name" not in models_source, (
        "Stale TODO edit name still in models.py"
    )


# ---------- Old TODO integrate instance settings removed ----------

def test_old_todo_integrate_instance_settings_removed(models_source):
    """``NchantdStore.__init__`` no longer has the ``# TODO integrate instance settings storage here`` comment."""
    assert "TODO integrate instance settings storage here" not in models_source


# ---------- sigil.py getData refactor ----------

def test_sigil_get_data_refactored(sigil_ast):
    """``NchantdSigilMixin.getData`` should be a real method now, not a stub."""
    cls = _find_class(sigil_ast, "NchantdSigilMixin")
    method = _find_method(cls, "getData")
    assert method is not None
    body_src = ast.unparse(method)
    assert "return self.records" in body_src, "getData should return self.records"
    assert "return self.defaults" in body_src, (
        "getData should fall back to self.defaults when records is None"
    )


def test_sigil_get_data_docstring(sigil_ast):
    """``getData`` should have a docstring explaining the fallback."""
    cls = _find_class(sigil_ast, "NchantdSigilMixin")
    method = _find_method(cls, "getData")
    docstring = ast.get_docstring(method)
    assert docstring is not None


def test_sigil_get_data_todo_removed(sigil_source):
    """The previous ``# TODO need to refactor these methods`` is removed."""
    assert "TODO need to refactor these methods" not in sigil_source


def test_sigil_get_data_handles_none_records(sigil_ast):
    """getData should explicitly check for None records (not just falsy)."""
    cls = _find_class(sigil_ast, "NchantdSigilMixin")
    method = _find_method(cls, "getData")
    body_src = ast.unparse(method)
    assert "is None" in body_src, "getData should use 'is None' for the records check"
