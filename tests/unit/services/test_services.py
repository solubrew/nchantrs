"""Tests for nchantrs services module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import os
import tempfile
from pathlib import Path


class TestDirectories:
    """Tests for directory service functionality."""
    
    def test_get_app_dir(self):
        """Test getting application directory."""
        from nchantrs.services.directories import get_app_dir
        
        result = get_app_dir()
        assert result is not None
        assert isinstance(result, (str, Path))
    
    def test_get_config_dir(self):
        """Test getting config directory."""
        from nchantrs.services.directories import get_config_dir
        
        result = get_config_dir()
        assert result is not None
        assert isinstance(result, (str, Path))
    
    def test_get_data_dir(self):
        """Test getting data directory."""
        from nchantrs.services.directories import get_data_dir
        
        result = get_data_dir()
        assert result is not None
        assert isinstance(result, (str, Path))
    
    def test_get_cache_dir(self):
        """Test getting cache directory."""
        from nchantrs.services.directories import get_cache_dir
        
        result = get_cache_dir()
        assert result is not None
        assert isinstance(result, (str, Path))


class TestIntegrity:
    """Tests for integrity service functionality."""
    
    def test_checksum_calculation(self):
        """Test checksum calculation."""
        from nchantrs.services.integrity import calculate_checksum
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            f.flush()
            temp_path = f.name
        
        try:
            checksum = calculate_checksum(temp_path)
            assert checksum is not None
            assert isinstance(checksum, str)
            assert len(checksum) > 0
        finally:
            os.unlink(temp_path)
    
    def test_verify_checksum_valid(self):
        """Test verifying valid checksum."""
        from nchantrs.services.integrity import calculate_checksum, verify_checksum
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            f.flush()
            temp_path = f.name
        
        try:
            checksum = calculate_checksum(temp_path)
            result = verify_checksum(temp_path, checksum)
            assert result is True
        finally:
            os.unlink(temp_path)
    
    def test_verify_checksum_invalid(self):
        """Test verifying invalid checksum."""
        from nchantrs.services.integrity import verify_checksum
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("test content")
            f.flush()
            temp_path = f.name
        
        try:
            result = verify_checksum(temp_path, "invalid_checksum")
            assert result is False
        finally:
            os.unlink(temp_path)


class TestBonds:
    """Tests for bonds service functionality."""
    
    def test_bond_creation(self):
        """Test creating a bond."""
        from nchantrs.services.bonds import create_bond
        
        result = create_bond("test_id", {"type": "test"})
        assert result is not None
    
    def test_get_bond(self):
        """Test getting a bond."""
        from nchantrs.services.bonds import create_bond, get_bond
        
        bond_data = {"type": "test", "name": "Test Bond"}
        create_bond("test_bond_id", bond_data)
        
        result = get_bond("test_bond_id")
        assert result is not None
    
    def test_list_bonds(self):
        """Test listing bonds."""
        from nchantrs.services.bonds import list_bonds
        
        result = list_bonds()
        assert isinstance(result, (list, dict))


class TestLinks:
    """Tests for links service functionality."""
    
    def test_create_link(self):
        """Test creating a link."""
        from nchantrs.services.links import create_link
        
        result = create_link("source", "target", "test_link")
        assert result is not None
    
    def test_get_link(self):
        """Test getting a link."""
        from nchantrs.services.links import get_link
        
        result = get_link("test_link_id")
        # May return None if not found
        assert result is None or isinstance(result, dict)
    
    def test_delete_link(self):
        """Test deleting a link."""
        from nchantrs.services.links import create_link, delete_link
        
        link_id = create_link("source", "target", "to_delete")
        result = delete_link(link_id)
        assert result is not None


class TestTags:
    """Tests for tags service functionality."""
    
    def test_create_tag(self):
        """Test creating a tag."""
        from nchantrs.services.tags import create_tag
        
        result = create_tag("test_tag", {"color": "blue"})
        assert result is not None
    
    def test_get_tag(self):
        """Test getting a tag."""
        from nchantrs.services.tags import get_tag
        
        result = get_tag("test_tag_id")
        # May return None if not found
        assert result is None or isinstance(result, dict)
    
    def test_list_tags(self):
        """Test listing tags."""
        from nchantrs.services.tags import list_tags
        
        result = list_tags()
        assert isinstance(result, (list, dict))
    
    def test_update_tag(self):
        """Test updating a tag."""
        from nchantrs.services.tags import create_tag, update_tag
        
        tag_id = create_tag("update_test", {"color": "red"})
        result = update_tag(tag_id, {"color": "green"})
        assert result is not None


class TestConnections:
    """Tests for connections service functionality."""
    
    def test_connection_creation(self):
        """Test creating a connection."""
        from nchantrs.services.connections import create_connection
        
        result = create_connection({"type": "test"})
        assert result is not None
    
    def test_get_connection(self):
        """Test getting a connection."""
        from nchantrs.services.connections import get_connection
        
        result = get_connection("test_conn_id")
        # May return None if not found
        assert result is None or isinstance(result, dict)
    
    def test_list_connections(self):
        """Test listing connections."""
        from nchantrs.services.connections import list_connections
        
        result = list_connections()
        assert isinstance(result, (list, dict))


class TestTelemetry:
    """Tests for telemetry service functionality."""
    
    @patch('nchantrs.services.telemetry.requests.post')
    def test_send_telemetry(self, mock_post):
        """Test sending telemetry data."""
        from nchantrs.services.telemetry import send_telemetry
        
        mock_post.return_value = Mock(status_code=200)
        
        result = send_telemetry({"event": "test"})
        assert result is True
    
    def test_telemetry_disabled_by_default(self):
        """Test that telemetry is disabled by default."""
        from nchantrs.services.telemetry import is_telemetry_enabled
        
        # Telemetry should be opt-in
        result = is_telemetry_enabled()
        assert result is False


class TestServices:
    """Tests for main services module."""
    
    def test_service_manager_creation(self):
        """Test creating service manager."""
        from nchantrs.services.services import ServicesManager
        
        manager = ServicesManager()
        assert manager is not None
    
    def test_get_service(self):
        """Test getting a service."""
        from nchantrs.services.services import ServicesManager
        
        manager = ServicesManager()
        service = manager.get_service("directories")
        assert service is not None
    
    def test_list_services(self):
        """Test listing services."""
        from nchantrs.services.services import ServicesManager
        
        manager = ServicesManager()
        services = manager.list_services()
        assert isinstance(services, (list, dict))


class TestProtocols:
    """Tests for protocol implementations."""
    
    def test_http_protocol_creation(self):
        """Test HTTP protocol creation."""
        from nchantrs.services.protocols.http import HTTPProtocol
        
        protocol = HTTPProtocol()
        assert protocol is not None
    
    @patch('httpx.Client')
    def test_http_get(self, mock_client):
        """Test HTTP GET request."""
        from nchantrs.services.protocols.http import HTTPProtocol
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        
        mock_instance = mock_client.return_value.__enter__.return_value
        mock_instance.get.return_value = mock_response
        
        protocol = HTTPProtocol()
        result = protocol.get("http://test.com")
        assert result.status_code == 200
    
    def test_mq_protocol_creation(self):
        """Test MQ protocol creation."""
        from nchantrs.services.protocols.mq import MQProtocol
        
        protocol = MQProtocol()
        assert protocol is not None
