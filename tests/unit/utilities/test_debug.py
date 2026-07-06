"""Tests for nchantrs debug utilities."""

import pytest
from unittest.mock import MagicMock, patch, mock_open
import logging


class TestDebugUtils:
    """Tests for debug utility functions."""

    def test_debug_logger_initialization(self):
        """Test debug logger can be initialized."""
        from nchantrs.utilities.debug import DebugLogger, setup_debug_logging
        
        # Test DebugLogger class exists and can be instantiated
        logger = DebugLogger("test_logger")
        assert logger.name == "test_logger"

    def test_setup_debug_logging(self):
        """Test debug logging setup function."""
        from nchantrs.utilities.debug import setup_debug_logging
        
        # Should not raise
        result = setup_debug_logging()
        assert result is not None


class TestDebugHelpers:
    """Tests for debug helper functions."""

    def test_format_traceback(self):
        """Test traceback formatting."""
        from nchantrs.utilities.debug import format_traceback
        import sys
        
        try:
            raise ValueError("Test error")
        except ValueError:
            result = format_traceback(sys.exc_info())
            assert isinstance(result, str)
            assert "ValueError" in result

    def test_log_exception(self):
        """Test exception logging."""
        from nchantrs.utilities.debug import log_exception
        
        logger = logging.getLogger("test")
        try:
            raise RuntimeError("Test exception")
        except RuntimeError:
            # Should not raise
            log_exception(logger, "Test context")


class TestDataSourceDump:
    """Tests for data source dump functionality."""

    def test_dump_data_source_structure(self):
        """Test data source dump creates proper structure."""
        from nchantrs.utilities.debug import DataSourceDump
        
        dump = DataSourceDump()
        assert hasattr(dump, "data")
        assert hasattr(dump, "add_entry")
        assert hasattr(dump, "to_dict")

    def test_dump_add_entry(self):
        """Test adding entries to dump."""
        from nchantrs.utilities.debug import DataSourceDump
        
        dump = DataSourceDump()
        dump.add_entry("test_source", {"key": "value"})
        
        result = dump.to_dict()
        assert "test_source" in result
        assert result["test_source"]["key"] == "value"
