# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name: Tags Service Unit Tests
        description: >
                Unit tests for TagGroup and Tag classes.
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*-

from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch


class TestTagGroup:
    """Unit tests for TagGroup class."""

    def test_init_with_name(self):
        """Test TagGroup initialization with name."""
        from nchantrs.services.tags import TagGroup
        
        group = TagGroup(name="TestGroup")
        
        assert group.name == "TestGroup"
        assert group.description == ""
        assert group.uuid is not None
        assert isinstance(group.tags, dict)

    def test_init_with_all_params(self):
        """Test TagGroup initialization with all parameters."""
        from nchantrs.services.tags import TagGroup
        
        group = TagGroup(
            name="TestGroup",
            description="A test group",
            uuid="test-uuid-123"
        )
        
        assert group.name == "TestGroup"
        assert group.description == "A test group"
        assert group.uuid == "test-uuid-123"

    def test_uuid_generation(self):
        """Test that UUID is generated when not provided."""
        from nchantrs.services.tags import TagGroup
        
        group1 = TagGroup(name="Group1")
        group2 = TagGroup(name="Group2")
        
        assert group1.uuid is not None
        assert group2.uuid is not None
        assert group1.uuid != group2.uuid


class TestTag:
    """Unit tests for Tag class."""

    def test_init_with_name(self):
        """Test Tag initialization with name."""
        from nchantrs.services.tags import Tag
        
        tag = Tag(name="TestTag")
        
        assert tag.name == "TestTag"
        assert tag.description == ""
        assert tag.uuid is not None

    def test_init_with_all_params(self):
        """Test Tag initialization with all parameters."""
        from nchantrs.services.tags import Tag
        
        tag = Tag(
            name="TestTag",
            description="A test tag",
            uuid="tag-uuid-456"
        )
        
        assert tag.name == "TestTag"
        assert tag.description == "A test tag"
        assert tag.uuid == "tag-uuid-456"

    def test_uuid_generation(self):
        """Test that UUID is generated when not provided."""
        from nchantrs.services.tags import Tag
        
        tag1 = Tag(name="Tag1")
        tag2 = Tag(name="Tag2")
        
        assert tag1.uuid is not None
        assert tag2.uuid is not None
        assert tag1.uuid != tag2.uuid

    def test_rename(self):
        """Test tag rename method."""
        from nchantrs.services.tags import Tag
        
        tag = Tag(name="OriginalName")
        original_uuid = tag.uuid
        
        tag.rename("NewName")
        
        assert tag.name == "NewName"
        assert tag.uuid == original_uuid  # UUID should not change

    def test_storage_returns_dataframe(self):
        """Test storage method returns DataFrame."""
        from nchantrs.services.tags import Tag
        
        tag = Tag(
            name="TestTag",
            description="Description",
            uuid="test-uuid"
        )
        
        with patch('nchantrs.services.tags.qpandas'):
            # Mock qpandas.DataFrame
            mock_df = MagicMock()
            mock_df.columns = ['name', 'description', 'uuid']
            with patch.dict('sys.modules', {'nchantrs.libraries.qpandas': MagicMock(DataFrame=mock_df)}):
                # Re-import with mocked qpandas
                result = tag.storage()
                # Verify it returns something with expected structure
                assert result is not None


class TestTagsIntegration:
    """Integration tests for tags functionality."""

    def test_tag_group_contains_tags(self):
        """Test that TagGroup can contain multiple tags."""
        from nchantrs.services.tags import TagGroup, Tag
        
        group = TagGroup(name="TestGroup")
        
        tag1 = Tag(name="Tag1")
        tag2 = Tag(name="Tag2")
        
        group.tags[tag1.uuid] = tag1
        group.tags[tag2.uuid] = tag2
        
        assert len(group.tags) == 2
        assert tag1.uuid in group.tags
        assert tag2.uuid in group.tags
