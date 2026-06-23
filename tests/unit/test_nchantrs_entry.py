"""Unit tests for nchantrs entry point functions."""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock
from pathlib import Path


class TestAberration:
    """Tests for the aberration entry point function."""

    @patch('nchantrs.dialogs.dialogs.NchantdClip')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_aberration_basic_call(self, mock_configure, mock_clip):
        """Test aberration function with basic parameters."""
        from nchantrs.nchantrs import aberration
        
        # Setup mocks
        mock_clip_instance = MagicMock()
        mock_clip.return_value = mock_clip_instance
        
        # Execute
        aberration("test_widget", {"arg": "value"}, widget="test")
        
        # Verify
        mock_clip.assert_called_once()
        mock_clip_instance.initApp.assert_called_once()

    @patch('nchantrs.dialogs.dialogs.NchantdClip')
    def test_aberration_with_none_cfg(self, mock_clip):
        """Test aberration function with None configuration."""
        from nchantrs.nchantrs import aberration
        
        mock_clip_instance = MagicMock()
        mock_clip.return_value = mock_clip_instance
        
        aberration("test_widget", None, widget="test", cfg=None)
        
        # Verify cfg was set properly
        call_kwargs = mock_clip.call_args[1]
        assert call_kwargs['cfg']['widget'] == "test"


class TestDistortion:
    """Tests for the distortion entry point function."""

    @patch('nchantrs.dialogs.dialogs.NchantdCape')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_distortion_basic_call(self, mock_configure, mock_cape):
        """Test distortion function with basic parameters."""
        from nchantrs.nchantrs import distortion
        
        mock_cape_instance = MagicMock()
        mock_cape_instance.initApp.return_value = {"result": "success"}
        mock_cape.return_value = mock_cape_instance
        
        result = distortion("test_widget", {"arg": "value"}, "test_widget", cfg={})
        
        assert result == {"result": "success"}
        mock_cape_instance.initApp.assert_called_once()

    @patch('nchantrs.dialogs.dialogs.NchantdCape')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_distortion_with_log_file(self, mock_configure, mock_cape):
        """Test distortion function with log file parameter."""
        from nchantrs.nchantrs import distortion
        
        mock_cape_instance = MagicMock()
        mock_cape_instance.initApp.return_value = True
        mock_cape.return_value = mock_cape_instance
        
        result = distortion(
            "test_widget", 
            {"arg": "value"}, 
            "test_widget", 
            cfg={"setting": True},
            log_file="/tmp/test.log"
        )
        
        # Verify log file was passed
        call_kwargs = mock_cape.call_args[1]
        assert call_kwargs['log_file'] == "/tmp/test.log"

    @patch('nchantrs.dialogs.dialogs.NchantdCape')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_distortion_with_instance(self, mock_configure, mock_cape):
        """Test distortion function with instance parameter."""
        from nchantrs.nchantrs import distortion
        
        mock_cape_instance = MagicMock()
        mock_cape_instance.initApp.return_value = True
        mock_cape.return_value = mock_cape_instance
        
        result = distortion(
            "test_widget", 
            {"arg": "value", "instance": "my_instance"}, 
            "test_widget",
            instance="my_instance"
        )
        
        # Verify instance was passed
        call_kwargs = mock_cape.call_args[1]
        assert call_kwargs['instance'] == "my_instance"


class TestNchantment:
    """Tests for the nchantment entry point function."""

    @patch('nchantrs.widgets.applications.applications.NchantdCloak')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_nchantment_basic_call(self, mock_configure, mock_cloak):
        """Test nchantment function with basic parameters."""
        from nchantrs.nchantrs import nchantment
        
        mock_cloak_instance = MagicMock()
        mock_cloak_instance.initApp.return_value = True
        mock_cloak.return_value = mock_cloak_instance
        
        result = nchantment("test_app", {"arg": "value"}, profile="default")
        
        assert result is True
        mock_cloak_instance.initApp.assert_called_once()

    @patch('nchantrs.widgets.applications.applications.NchantdCloak')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_nchantment_with_instance_in_args(self, mock_configure, mock_cloak):
        """Test nchantment function extracts instance from args."""
        from nchantrs.nchantrs import nchantment
        
        mock_cloak_instance = MagicMock()
        mock_cloak_instance.initApp.return_value = True
        mock_cloak.return_value = mock_cloak_instance
        
        result = nchantment("test_app", {"instance": "custom_instance"}, profile="default")
        
        # Verify instance was extracted from args
        call_kwargs = mock_cloak.call_args[1]
        assert call_kwargs['instance'] == "custom_instance"

    @patch('nchantrs.widgets.applications.applications.NchantdCloak')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_nchantment_with_profile_override(self, mock_configure, mock_cloak):
        """Test nchantment function with profile override."""
        from nchantrs.nchantrs import nchantment
        
        mock_cloak_instance = MagicMock()
        mock_cloak_instance.initApp.return_value = True
        mock_cloak.return_value = mock_cloak_instance
        
        result = nchantment("test_app", {"profile": "override_profile"}, profile="default")
        
        # Verify profile from args overrides parameter
        call_kwargs = mock_cloak.call_args[1]
        assert call_kwargs['profile'] == "override_profile"


class TestFlection:
    """Tests for the flection entry point function."""

    @patch('nchantrs.widgets.applications.applications.NchantdCloak')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    @patch('nchantrs.nchantrs.pyularity')
    def test_flection_with_pyularity_available(self, mock_pyularity, mock_configure, mock_cloak):
        """Test flection function when pyularity is available."""
        from nchantrs.nchantrs import flection
        
        mock_pyularity.is_available.return_value = True
        mock_cloak_instance = MagicMock()
        mock_cloak_instance.initApp.return_value = True
        mock_cloak.return_value = mock_cloak_instance
        
        result = flection("test_app", {"arg": "value"})
        
        assert result is True
        mock_cloak_instance.initApp.assert_called_once()

    @patch('nchantrs.widgets.applications.applications.NchantdCloak')
    @patch('nchantrs.widgets.browsers.initialize._configure_qt_environment')
    def test_flection_fallback_without_pyularity(self, mock_configure, mock_cloak):
        """Test flection function falls back when pyularity not available."""
        from nchantrs.nchantrs import flection
        
        # Simulate pyularity not being available
        with patch.dict('sys.modules', {'pyularity': None}):
            mock_cloak_instance = MagicMock()
            mock_cloak_instance.initApp.return_value = True
            mock_cloak.return_value = mock_cloak_instance
            
            result = flection("test_app", {"arg": "value"})
            
            assert result is True


class TestMemoryAnalysis:
    """Tests for memory analysis functions."""

    def test_analyze_strings_no_error(self):
        """Test analyze_strings handles case when no data available."""
        from nchantrs.nchantrs import _analyze_strings
        
        result = _analyze_strings(None)
        
        # Should not raise an error
        assert result is None or isinstance(result, str)

    def test_analyze_strings_with_data(self):
        """Test analyze_strings processes string data."""
        from nchantrs.nchantrs import _analyze_strings
        
        test_data = "test string data"
        result = _analyze_strings(test_data)
        
        # Should process the data without error
        assert result is not False

    def test_memory_analysis_guppy_not_available(self):
        """Test memory analysis when guppy is not available."""
        from nchantrs.nchantrs import _memory_analysis
        
        # Ensure guppy is not available
        with patch.dict('sys.modules', {'guppy': None}):
            with patch('nchantrs.nchantrs.tracemalloc') as mock_tracemalloc:
                mock_tracemalloc.get_traced_memory.return_value = (1024, 2048)
                mock_tracemalloc.start.return_value = None
                mock_tracemalloc.stop.return_value = None
                
                result = _memory_analysis()
                
                # Should complete without error
                assert result is not False

    def test_memory_summary_pympler_not_available(self):
        """Test memory summary when pympler is not available."""
        from nchantrs.nchantrs import _memory_summary
        
        with patch.dict('sys.modules', {'pympler': None}):
            result = _memory_summary()
            
            # Should return False or handle gracefully
            assert result is None or result is False or isinstance(result, str)
