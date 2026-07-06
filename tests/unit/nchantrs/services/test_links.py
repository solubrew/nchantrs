"""Unit tests for LinksService."""

import pytest
from unittest.mock import MagicMock, patch


class TestLinksService:
    """Test cases for LinksService."""

    def test_init_default(self):
        """Test service initialization with defaults."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        
        assert service.name == "LinksService"
        assert service._links == {}

    def test_init_with_config(self):
        """Test service initialization with config."""
        from nchantrs.services.links import LinksService
        
        config = {"max_links": 100}
        service = LinksService(config=config)
        
        assert service.config == config

    def test_add_link_empty_source(self):
        """Test adding link with empty source."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        result = service.add_link("", "target", "default")
        
        assert result is False

    def test_add_link_empty_target(self):
        """Test adding link with empty target."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        result = service.add_link("source", "", "default")
        
        assert result is False

    def test_add_link_none_source(self):
        """Test adding link with None source."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        result = service.add_link(None, "target", "default")
        
        assert result is False

    def test_add_link_success(self):
        """Test successfully adding a link."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        result = service.add_link("source1", "target1", "default")
        
        assert result is True
        assert "default" in service._links
        assert "source1->target1" in service._links["default"]

    def test_add_link_duplicate(self):
        """Test adding duplicate link."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        service.add_link("source1", "target1", "default")
        result = service.add_link("source1", "target1", "default")
        
        assert result is False

    def test_add_link_custom_type(self):
        """Test adding link with custom type."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        result = service.add_link("src", "tgt", "custom_type")
        
        assert result is True
        assert "custom_type" in service._links

    def test_remove_link_not_found(self):
        """Test removing non-existent link."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        result = service.remove_link("source", "target", "default")
        
        assert result is False

    def test_remove_link_wrong_type(self):
        """Test removing link from wrong type."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        service.add_link("source", "target", "type1")
        result = service.remove_link("source", "target", "type2")
        
        assert result is False

    def test_remove_link_success(self):
        """Test successfully removing a link."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        service.add_link("source", "target", "default")
        result = service.remove_link("source", "target", "default")
        
        assert result is True
        assert "source->target" not in service._links.get("default", [])

    def test_get_links_empty(self):
        """Test getting links when none exist."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        links = service.get_links("default")
        
        assert links == []

    def test_get_links_with_data(self):
        """Test getting links with existing data."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        service.add_link("source1", "target1", "default")
        service.add_link("source2", "target2", "default")
        links = service.get_links("default")
        
        assert len(links) == 2
        assert "source1->target1" in links
        assert "source2->target2" in links

    def test_get_links_specific_type(self):
        """Test getting links of specific type."""
        from nchantrs.services.links import LinksService
        
        service = LinksService()
        service.add_link("src1", "tgt1", "type1")
        service.add_link("src2", "tgt2", "type2")
        
        links1 = service.get_links("type1")
        links2 = service.get_links("type2")
        
        assert links1 == ["src1->tgt1"]
        assert links2 == ["src2->tgt2"]
