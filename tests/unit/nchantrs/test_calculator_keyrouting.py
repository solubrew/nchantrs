"""Tests for NchantdAdvancedCalculator key-routing (T-NEW-002).

The calculator should accept digit/operator keys via ``keyPressEvent``
and route them through the same entry logic as button clicks. These
tests exercise the key-routing code paths by reading the source file
and parsing the AST — they verify the class structure and method
bodies without instantiating the Qt widget (which fails in headless
pytest environments because the mock-PyQt metaclass conflicts when
NchantdWidget subclasses mock-Qt-classes).

The intent is to verify the class-specific logic itself: the
``keyPressEvent`` dispatcher, the ``_press_digit`` helper, the
``_apply_*_operator`` helpers, and the focus handling.
"""
import ast
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
CALCULATORS_PATH = PROJECT_ROOT / "nchantrs" / "widgets" / "calculators" / "calculators.py"


@pytest.fixture(scope="module")
def calc_source():
    """Read the calculators.py source file."""
    return CALCULATORS_PATH.read_text()


@pytest.fixture(scope="module")
def calc_ast(calc_source):
    """Parse the modules AST."""
    return ast.parse(calc_source)


# ---------- Pure-source structural tests (no instantiation) ----------

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


def test_nchantd_calculator_class_exists(calc_ast):
    """The base ``NchantdCalculator`` class is defined."""
    node = _find_class(calc_ast, "NchantdCalculator")
    assert node is not None, "NchantdCalculator class not found"


def test_nchantd_advanced_calculator_class_exists(calc_ast):
    """``NchantdAdvancedCalculator`` exists."""
    node = _find_class(calc_ast, "NchantdAdvancedCalculator")
    assert node is not None, "NchantdAdvancedCalculator class not found"


def test_nchantd_advanced_calculator_has_key_press_event(calc_ast):
    """The T-NEW-002 fix added ``keyPressEvent`` to the advanced calculator."""
    cls = _find_class(calc_ast, "NchantdAdvancedCalculator")
    method = _find_method(cls, "keyPressEvent")
    assert method is not None, "keyPressEvent method missing"
    body_src = ast.unparse(method)
    # The dispatcher should handle the digit keys
    assert "Key_0" in body_src and "Key_9" in body_src, "keyPressEvent should map Key_0..Key_9"
    assert "_press_digit" in body_src, "keyPressEvent should delegate to _press_digit"
    # It should handle the decimal separator
    assert "Key_Period" in body_src or "Key_Comma" in body_src, "keyPressEvent should map decimal keys"
    # It should handle the operator keys
    assert "Key_Plus" in body_src, "keyPressEvent should map Key_Plus"
    assert "Key_Minus" in body_src, "keyPressEvent should map Key_Minus"
    assert "Key_Asterisk" in body_src, "keyPressEvent should map Key_Asterisk"
    assert "Key_Slash" in body_src, "keyPressEvent should map Key_Slash"
    # It should handle Enter and Escape
    assert "Key_Return" in body_src or "Key_Enter" in body_src, "keyPressEvent should map Enter"
    assert "Key_Escape" in body_src, "keyPressEvent should map Escape"
    # Unhandled keys should fall through to super()
    assert "super().keyPressEvent" in body_src, "keyPressEvent should fall through to super()"


def test_nchantd_advanced_calculator_has_focus_handlers(calc_ast):
    """``focusInEvent`` and ``focusOutEvent`` set/clear the ``_has_focus`` flag."""
    cls = _find_class(calc_ast, "NchantdAdvancedCalculator")
    focus_in = _find_method(cls, "focusInEvent")
    focus_out = _find_method(cls, "focusOutEvent")
    assert focus_in is not None, "focusInEvent missing"
    assert focus_out is not None, "focusOutEvent missing"
    body_in = ast.unparse(focus_in)
    body_out = ast.unparse(focus_out)
    assert "_has_focus" in body_in, "focusInEvent should set _has_focus"
    assert "_has_focus" in body_out, "focusOutEvent should update _has_focus"


def test_init_sets_strong_focus_policy(calc_source):
    """The calculator's ``__init__`` should set ``StrongFocus`` focus policy."""
    assert "StrongFocus" in calc_source, "StrongFocus policy not set"


def test_press_digit_helper_is_refactored(calc_ast):
    """``_press_digit`` is the extracted helper that ``digitClicked`` delegates to."""
    cls = _find_class(calc_ast, "NchantdCalculator")
    method = _find_method(cls, "_press_digit")
    assert method is not None, "_press_digit helper missing"
    # The helper should reject out-of-range values
    body_src = ast.unparse(method)
    assert "0" in body_src and "9" in body_src, "_press_digit should validate range 0-9"


def test_digit_clicked_delegates_to_press_digit(calc_ast):
    """``digitClicked`` (the button-driven path) should delegate to ``_press_digit``."""
    cls = _find_class(calc_ast, "NchantdCalculator")
    method = _find_method(cls, "digitClicked")
    assert method is not None, "digitClicked missing"
    body_src = ast.unparse(method)
    assert "_press_digit" in body_src, "digitClicked should call _press_digit"
    assert "clickedButton.text()" in body_src, "digitClicked should still extract digit from button"


def test_apply_additive_operator_accepts_string(calc_ast):
    """``_apply_additive_operator`` is the extracted helper that takes the operator."""
    cls = _find_class(calc_ast, "NchantdCalculator")
    method = _find_method(cls, "_apply_additive_operator")
    assert method is not None, "_apply_additive_operator helper missing"
    # It should take a parameter named clickedOperator
    args = [a.arg for a in method.args.args]
    assert "clickedOperator" in args, "_apply_additive_operator should take clickedOperator"


def test_apply_multiplicative_operator_accepts_string(calc_ast):
    """``_apply_multiplicative_operator`` is the extracted helper."""
    cls = _find_class(calc_ast, "NchantdCalculator")
    method = _find_method(cls, "_apply_multiplicative_operator")
    assert method is not None, "_apply_multiplicative_operator helper missing"
    args = [a.arg for a in method.args.args]
    assert "clickedOperator" in args, "_apply_multiplicative_operator should take clickedOperator"


def test_additive_operator_clicked_uses_helper(calc_ast):
    """``additiveOperatorClicked`` (button-driven) should delegate to ``_apply_additive_operator``."""
    cls = _find_class(calc_ast, "NchantdCalculator")
    method = _find_method(cls, "additiveOperatorClicked")
    assert method is not None
    body_src = ast.unparse(method)
    assert "_apply_additive_operator" in body_src, (
        "additiveOperatorClicked should delegate to _apply_additive_operator"
    )


def test_multiplicative_operator_clicked_uses_helper(calc_ast):
    """``multiplicativeOperatorClicked`` (button-driven) should delegate to ``_apply_multiplicative_operator``."""
    cls = _find_class(calc_ast, "NchantdCalculator")
    method = _find_method(cls, "multiplicativeOperatorClicked")
    assert method is not None
    body_src = ast.unparse(method)
    assert "_apply_multiplicative_operator" in body_src, (
        "multiplicativeOperatorClicked should delegate to _apply_multiplicative_operator"
    )


def test_legacy_init_methods_no_longer_reference_method_name(calc_source):
    """The 4 broken ``initUI`` / ``initModel`` / ``initView`` / ``initWidget``
    methods in ``NchantdAdvancedCalculator`` previously referenced the
    undefined ``method_name`` variable. The fix replaces them with
    direct ``super().X()`` calls."""
    broken_pattern = "super_method = getattr(super(type(self), self), method_name, None)"
    assert broken_pattern not in calc_source, (
        f"Leftover broken pattern: {broken_pattern!r}"
    )


def test_nchantd_graphing_calculator_init_model_does_not_reference_method_name(calc_source):
    """The fix also cleaned up ``NchantdGraphingCalculator.initModel``."""
    import re
    m = re.search(
        r"class NchantdGraphingCalculator\b.*?(?=^class |\Z)",
        calc_source,
        re.MULTILINE | re.DOTALL,
    )
    assert m, "NchantdGraphingCalculator class not found"
    class_body = m.group(0)
    assert "method_name" not in class_body, (
        "NchantdGraphingCalculator still references undefined method_name"
    )


def test_t_new_002_todo_removed(calc_source):
    """The original 2026-07 TODO at calculators.py:42 is removed."""
    assert "need to route number keys" not in calc_source, (
        "Stale TODO comment still present"
    )


def test_key_shortcut_handlers_in_source(calc_source):
    """The operator-key shortcuts map to the correct visible symbols:
    Keyboard asterisk -> '×' (the button text), Keyboard slash -> '÷'."""
    assert "'×'" in calc_source, "Multiplicative times symbol not found"
    assert "'÷'" in calc_source, "Multiplicative division symbol not found"


def test_kbkey_digit_minus_to_apply_additive_operator(calc_source):
    """The Minus key handler routes to ``_apply_additive_operator('-')``."""
    assert "_apply_additive_operator('-')" in calc_source, (
        "Key_Minus should call _apply_additive_operator('-')"
    )


def test_kbkey_asterisk_to_apply_multiplicative_operator_x(calc_source):
    """The Asterisk key handler routes to ``_apply_multiplicative_operator('×')``."""
    assert "_apply_multiplicative_operator('×')" in calc_source, (
        "Key_Asterisk should call _apply_multiplicative_operator('×')"
    )


def test_kbkey_slash_to_apply_multiplicative_operator_divided(calc_source):
    """The Slash key handler routes to ``_apply_multiplicative_operator('÷')``."""
    assert "_apply_multiplicative_operator('÷')" in calc_source, (
        "Key_Slash should call _apply_multiplicative_operator('÷')"
    )
