"""Tests for NchantdStore class."""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
import tempfile
import os
from pathlib import Path


class TestTableNameResolver:
    """Test TableNameResolver class."""

    def test_resolver_import(self):
        """Test that TableNameResolver can be imported."""
        from nchantrs.models.models import TableNameResolver
        assert TableNameResolver is not None

    def test_resolver_initialization(self):
        """Test TableNameResolver initialization."""
        from nchantrs.models.models import TableNameResolver
        
        resolver = TableNameResolver()
        assert resolver is not None
        assert hasattr(resolver, '_cache')
        assert resolver._cache == {}

    def test_get_table_name_basic(self):
        """Test basic table name resolution."""
        from nchantrs.models.models import TableNameResolver
        
        resolver = TableNameResolver()
        table_name = resolver.get_table_name("users")
        
        assert table_name == "vw_users"

    def test_get_table_name_caching(self):
        """Test that table names are cached."""
        from nchantrs.models.models import TableNameResolver
        
        resolver = TableNameResolver()
        name1 = resolver.get_table_name("users")
        name2 = resolver.get_table_name("users")
        
        assert name1 == name2
        assert len(resolver._cache) == 1

    def test_clear_cache(self):
        """Test cache clearing."""
        from nchantrs.models.models import TableNameResolver
        
        resolver = TableNameResolver()
        resolver.get_table_name("users")
        assert len(resolver._cache) == 1
        
        resolver.clear_cache()
        assert len(resolver._cache) == 0


class TestPayloadBuilder:
    """Test PayloadBuilder class."""

    def test_payload_builder_import(self):
        """Test that PayloadBuilder can be imported."""
        from nchantrs.models.models import PayloadBuilder
        assert PayloadBuilder is not None

    def test_validate_valid_operations(self):
        """Test validation of valid operations."""
        from nchantrs.models.models import PayloadBuilder
        
        valid_ops = ["INSERT", "UPDATE", "DEACTIVATE", "DELETE", "ARCHIVE"]
        for op in valid_ops:
            result = PayloadBuilder.validate_and_get_operation(op)
            assert result == op

    def test_validate_invalid_operation(self):
        """Test validation of invalid operation raises error."""
        from nchantrs.models.models import PayloadBuilder
        
        with pytest.raises(ValueError):
            PayloadBuilder.validate_and_get_operation("INVALID_OP")

    def test_build_cfg_payload(self):
        """Test payload configuration building."""
        from nchantrs.models.models import PayloadBuilder
        
        records = [{"id": 1, "name": "test"}]
        payload = PayloadBuilder.build_cfg_payload("users", records)
        
        assert "table" in payload
        assert "users" in payload["table"]
        assert payload["table"]["users"]["records"] == records

    def test_build_cfg_payload_with_columns(self):
        """Test payload configuration building with columns."""
        from nchantrs.models.models import PayloadBuilder
        
        records = [{"id": 1, "name": "test"}]
        columns = ["id", "name"]
        payload = PayloadBuilder.build_cfg_payload("users", records, columns)
        
        assert payload["table"]["users"]["columns"] == columns


class TestWindowPolicyParser:
    """Test WindowPolicyParser class."""

    def test_parser_import(self):
        """Test that WindowPolicyParser can be imported."""
        from nchantrs.models.models import WindowPolicyParser
        assert WindowPolicyParser is not None

    def test_parse_days(self):
        """Test parsing days window."""
        from nchantrs.models.models import WindowPolicyParser
        
        mock_time = MagicMock()
        parser = WindowPolicyParser(mock_time)
        
        result = parser.parse("30DAYS")
        assert result == (30, "days")

    def test_parse_weeks(self):
        """Test parsing weeks window."""
        from nchantrs.models.models import WindowPolicyParser
        
        mock_time = MagicMock()
        parser = WindowPolicyParser(mock_time)
        
        result = parser.parse("2WEEKS")
        assert result == (2, "weeks")

    def test_parse_months(self):
        """Test parsing months window."""
        from nchantrs.models.models import WindowPolicyParser
        
        mock_time = MagicMock()
        parser = WindowPolicyParser(mock_time)
        
        result = parser.parse("3MONTHS")
        assert result == (3, "months")

    def test_parse_years(self):
        """Test parsing years window."""
        from nchantrs.models.models import WindowPolicyParser
        
        mock_time = MagicMock()
        parser = WindowPolicyParser(mock_time)
        
        result = parser.parse("1YEARS")
        assert result == (1, "years")

    def test_parse_invalid_window(self):
        """Test parsing invalid window raises error."""
        from nchantrs.models.models import WindowPolicyParser
        
        mock_time = MagicMock()
        parser = WindowPolicyParser(mock_time)
        
        with pytest.raises(ValueError):
            parser.parse("INVALID")

    def test_parse_caching(self):
        """Test that parsed windows are cached."""
        from nchantrs.models.models import WindowPolicyParser
        
        mock_time = MagicMock()
        parser = WindowPolicyParser(mock_time)
        
        parser.parse("30DAYS")
        assert "30DAYS" in parser._cache
        
        parser.parse("30DAYS")
        # Should not re-parse, just return cached
        assert len(parser._cache) == 1


class TestNchantdInstance:
    """Test NchantdInstance class."""

    def test_instance_import(self):
        """Test that NchantdInstance can be imported."""
        from nchantrs.models.models import NchantdInstance
        assert NchantdInstance is not None

    def test_instance_initialization(self):
        """Test NchantdInstance initialization with mock parent."""
        from nchantrs.models.models import NchantdInstance
        
        mock_parent = MagicMock()
        mock_parent.app.application_NCD = "test_app"
        mock_parent.app.model.application_path = "/tmp/test"
        mock_parent.app.model.slug = "test"
        mock_parent.app.model.store.EXTENSION = ".sqlite"
        mock_parent.app.model.get_current_version = MagicMock(return_value="1.0.0")
        
        instance = NchantdInstance(parent=mock_parent)
        
        assert instance is not None
        assert instance.is_new == True
        assert instance.instance_id is not None

    def test_set_instance_id_generates_new(self):
        """Test that set_instance_id generates new ID when None."""
        from nchantrs.models.models import NchantdInstance
        
        mock_parent = MagicMock()
        mock_parent.app.application_NCD = "test_app"
        mock_parent.app.model.application_path = "/tmp/test"
        mock_parent.app.model.slug = "test"
        mock_parent.app.model.store.EXTENSION = ".sqlite"
        mock_parent.app.model.get_current_version = MagicMock(return_value="1.0.0")
        
        instance = NchantdInstance(parent=mock_parent, cfg={})
        
        assert instance.instance_id is not None
        assert instance.db_instance_id is not None
        assert instance.dbc_instance_id is not None

    def test_set_name(self):
        """Test setting instance name."""
        from nchantrs.models.models import NchantdInstance
        
        mock_parent = MagicMock()
        mock_parent.app.application_NCD = "test_app"
        mock_parent.app.model.application_path = "/tmp/test"
        mock_parent.app.model.slug = "test"
        mock_parent.app.model.store.EXTENSION = ".sqlite"
        mock_parent.app.model.get_current_version = MagicMock(return_value="1.0.0")
        
        instance = NchantdInstance(parent=mock_parent, cfg={})
        instance.set_name("Test Instance")
        
        assert instance.name == "Test Instance"

    def test_set_independent(self):
        """Test setting instance as independent."""
        from nchantrs.models.models import NchantdInstance
        
        mock_parent = MagicMock()
        mock_parent.app.application_NCD = "test_app"
        mock_parent.app.model.application_path = "/tmp/test"
        mock_parent.app.model.slug = "test"
        mock_parent.app.model.store.EXTENSION = ".sqlite"
        mock_parent.app.model.get_current_version = MagicMock(return_value="1.0.0")
        
        instance = NchantdInstance(parent=mock_parent, cfg={})
        instance.set_independent(True)
        
        assert instance.is_independent == True
