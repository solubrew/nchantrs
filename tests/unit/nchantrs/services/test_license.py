"""Unit tests for LicenseService."""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch


class TestLicenseService:
    """Test cases for LicenseService."""

    def test_init_default(self):
        """Test service initialization with defaults."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        
        assert service.name == "LicenseService"
        assert service._license_data == {}
        assert service._valid is False

    def test_init_with_config(self):
        """Test service initialization with config."""
        from nchantrs.services.license import LicenseService
        
        config = {"debug": True}
        service = LicenseService(config=config)
        
        assert service.config == config

    def test_load_license_empty_key(self):
        """Test loading empty license key."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        result = service.load_license("")
        
        assert result is False
        assert service._valid is False

    def test_load_license_none_key(self):
        """Test loading None license key."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        result = service.load_license(None)
        
        assert result is False

    def test_load_license_valid(self):
        """Test loading valid license key."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        result = service.load_license("TEST-LICENSE-KEY-12345")
        
        assert result is True
        assert service._valid is True
        assert "key" in service._license_data
        assert service._license_data["key"] == "TEST-LICENSE-KEY-12345"
        assert "loaded_at" in service._license_data
        assert isinstance(service._license_data["loaded_at"], datetime)

    def test_validate_no_license(self):
        """Test validation with no license loaded."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        result = service.validate_license()
        
        assert result is False

    def test_validate_invalid(self):
        """Test validation when license is invalid."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        service._license_data = {"key": "test"}
        service._valid = False
        result = service.validate_license()
        
        assert result is False

    def test_validate_valid(self):
        """Test validation when license is valid."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        service.load_license("VALID-KEY")
        result = service.validate_license()
        
        assert result is True

    def test_get_license_info_no_license(self):
        """Test getting info when no license loaded."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        info = service.get_license_info()
        
        assert info["valid"] is False
        assert info["loaded_at"] is None
        assert info["key_prefix"] is None

    def test_get_license_info_with_license(self):
        """Test getting info with license loaded."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        service.load_license("TEST-LICENSE-KEY")
        info = service.get_license_info()
        
        assert info["valid"] is True
        assert info["loaded_at"] is not None
        assert info["key_prefix"] == "TEST-LIC"

    def test_revoke_license(self):
        """Test revoking license."""
        from nchantrs.services.license import LicenseService
        
        service = LicenseService()
        service.load_license("TEST-KEY")
        service.revoke_license()
        
        assert service._license_data == {}
        assert service._valid is False
