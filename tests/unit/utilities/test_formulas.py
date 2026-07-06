"""Tests for nchantrs formula utilities."""

import pytest
from unittest.mock import MagicMock, patch


class TestFormulaParser:
    """Tests for formula parsing functionality."""

    def test_simple_arithmetic(self):
        """Test simple arithmetic expression parsing."""
        from nchantrs.utilities.formulas import FormulaParser
        
        parser = FormulaParser()
        result = parser.parse("2 + 3")
        assert result == 5

    def test_complex_expression(self):
        """Test complex expression parsing."""
        from nchantrs.utilities.formulas import FormulaParser
        
        parser = FormulaParser()
        result = parser.parse("(10 + 5) * 2")
        assert result == 30

    def test_division(self):
        """Test division handling."""
        from nchantrs.utilities.formulas import FormulaParser
        
        parser = FormulaParser()
        result = parser.parse("10 / 2")
        assert result == 5

    def test_formula_with_variables(self):
        """Test formula with variable substitution."""
        from nchantrs.utilities.formulas import FormulaParser
        
        parser = FormulaParser()
        vars_ = {"x": 10, "y": 5}
        result = parser.parse("x + y", variables=vars_)
        assert result == 15


class TestFormulaValidation:
    """Tests for formula validation."""

    def test_validate_valid_formula(self):
        """Test validation of valid formula."""
        from nchantrs.utilities.formulas import validate_formula
        
        result = validate_formula("A1 + B1")
        assert result is True

    def test_validate_invalid_formula(self):
        """Test validation catches invalid formulas."""
        from nchantrs.utilities.formulas import validate_formula
        
        result = validate_formula("A1 +")
        assert result is False

    def test_validate_empty_formula(self):
        """Test validation of empty formula."""
        from nchantrs.utilities.formulas import validate_formula
        
        result = validate_formula("")
        assert result is False


class TestFormulaFunctions:
    """Tests for built-in formula functions."""

    def test_sum_function(self):
        """Test SUM function."""
        from nchantrs.utilities.formulas import evaluate_function
        
        result = evaluate_function("SUM", [1, 2, 3, 4, 5])
        assert result == 15

    def test_average_function(self):
        """Test AVERAGE function."""
        from nchantrs.utilities.formulas import evaluate_function
        
        result = evaluate_function("AVERAGE", [10, 20, 30])
        assert result == 20

    def test_min_function(self):
        """Test MIN function."""
        from nchantrs.utilities.formulas import evaluate_function
        
        result = evaluate_function("MIN", [5, 3, 8, 1])
        assert result == 1

    def test_max_function(self):
        """Test MAX function."""
        from nchantrs.utilities.formulas import evaluate_function
        
        result = evaluate_function("MAX", [5, 3, 8, 1])
        assert result == 8

    def test_count_function(self):
        """Test COUNT function."""
        from nchantrs.utilities.formulas import evaluate_function
        
        result = evaluate_function("COUNT", [1, 2, 3, "text", None, 4])
        assert result == 4  # Only counts numeric values

    def test_if_function(self):
        """Test IF function."""
        from nchantrs.utilities.formulas import evaluate_function
        
        result = evaluate_function("IF", [True, "yes", "no"])
        assert result == "yes"
        
        result = evaluate_function("IF", [False, "yes", "no"])
        assert result == "no"

    def test_concat_function(self):
        """Test CONCAT function."""
        from nchantrs.utilities.formulas import evaluate_function
        
        result = evaluate_function("CONCAT", ["Hello", " ", "World"])
        assert result == "Hello World"

    def test_unknown_function(self):
        """Test unknown function raises error."""
        from nchantrs.utilities.formulas import evaluate_function
        
        with pytest.raises(ValueError):
            evaluate_function("UNKNOWN", [1, 2, 3])
