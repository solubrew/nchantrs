"""Unit tests for NchantrsService base class."""

import pytest
from unittest.mock import MagicMock, patch


class TestNchantrsService:
    """Test cases for NchantrsService base class."""

    def test_init_default_config(self):
        """Test service initialization with default config."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        
        assert service.config == {}
        assert service.name == "NchantrsService"
        assert service._initialized is False
        assert service._state == {}

    def test_init_with_config(self):
        """Test service initialization with custom config."""
        from nchantrs.services.services import NchantrsService
        
        config = {"debug": True, "timeout": 30}
        service = NchantrsService(config=config)
        
        assert service.config == config
        assert service.get_config("debug") is True
        assert service.get_config("timeout") == 30

    def test_initialize(self):
        """Test service initialization."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        result = service.initialize()
        
        assert result is True
        assert service.is_initialized is True

    def test_shutdown(self):
        """Test service shutdown."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        service.initialize()
        service.shutdown()
        
        assert service.is_initialized is False

    def test_get_config_with_default(self):
        """Test getting config with default value."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        
        assert service.get_config("nonexistent", "default") == "default"
        assert service.get_config("nonexistent") is None

    def test_set_config(self):
        """Test setting config values."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        service.set_config("key", "value")
        
        assert service.get_config("key") == "value"

    def test_validate(self):
        """Test service validation."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        assert service.validate() is True

    def test_health_check_not_initialized(self):
        """Test health check when service is not initialized."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        health = service.health_check()
        
        assert health["service"] == "NchantrsService"
        assert health["status"] == "not_initialized"
        assert health["state"] == {}

    def test_health_check_initialized(self):
        """Test health check when service is initialized."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        service.initialize()
        health = service.health_check()
        
        assert health["status"] == "healthy"

    def test_state_property(self):
        """Test state property returns copy."""
        from nchantrs.services.services import NchantrsService
        
        service = NchantrsService()
        service._state["test"] = "value"
        
        state = service.state
        state["test"] = "modified"
        
        assert service._state["test"] == "value"
