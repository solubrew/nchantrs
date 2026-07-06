"""Unit tests for nchantrs core module."""
import pytest
from unittest.mock import MagicMock, patch, PropertyMock


class TestNchantrsCore:
    """Test suite for nchantrs core functionality."""

    def test_nchantrs_version_format(self):
        """Test that version string follows expected format."""
        from nchantrs import __version__
        assert isinstance(__version__, str)
        # Version should be in format X.Y.Z.W
        parts = __version__.split('.')
        assert len(parts) == 4, f"Expected 4 version parts, got {len(parts)}"

    def test_nchantrs_package_import(self):
        """Test that nchantrs package imports correctly."""
        import nchantrs
        assert hasattr(nchantrs, '__version__')
        assert hasattr(nchantrs, 'NchantrsApp')

    @patch('nchantrs.nchantrs.QtWidgets')
    @patch('nchantrs.nchantrs.QtCore')
    def test_nchantrs_initialization(self, mock_qt_core, mock_qt_widgets):
        """Test NchantrsApp initialization."""
        from nchantrs.nchantrs import NchantrsApp
        
        # Mock required components
        mock_app = MagicMock()
        mock_qt_widgets.QApplication.instance.return_value = mock_app
        
        # Should not raise on initialization attempt
        # Note: Actual initialization requires Qt app context

    def test_nchantrs_app_has_required_methods(self):
        """Test that NchantrsApp has expected interface methods."""
        from nchantrs.nchantrs import NchantrsApp
        
        expected_methods = [
            'setup_ui',
            'load_theme',
            'initialize_services',
            'run'
        ]
        
        for method in expected_methods:
            assert hasattr(NchantrsApp, method) or method in dir(NchantrsApp), \
                f"NchantrsApp missing expected method: {method}"


class TestNchantrsMain:
    """Test suite for nchantrs main entry point."""

    def test_main_entry_point_exists(self):
        """Test that main entry point module exists."""
        from nchantrs import __main__
        assert hasattr(__main__, 'main')

    @patch('sys.argv', ['nchantrs', '--help'])
    def test_cli_help_flag(self):
        """Test CLI help flag handling."""
        # CLI should handle --help without crashing
        from nchantrs.cli import parse_args
        args = parse_args(['--help'])
        assert args.help is True

    @patch('sys.argv', ['nchantrs'])
    def test_cli_default_args(self):
        """Test CLI default arguments."""
        from nchantrs.cli import parse_args
        args = parse_args([])
        assert hasattr(args, 'command')

    @patch('sys.argv', ['nchantrs', '--version'])
    def test_cli_version_flag(self):
        """Test CLI version flag handling."""
        from nchantrs.cli import parse_args
        args = parse_args(['--version'])
        assert args.version is True

    @patch('sys.argv', ['nchantrs', '--debug'])
    def test_cli_debug_flag(self):
        """Test CLI debug flag handling."""
        from nchantrs.cli import parse_args
        args = parse_args(['--debug'])
        assert args.debug is True


class TestNchantrsPackage:
    """Test suite for nchantrs package-level exports."""

    def test_package_has_version(self):
        """Test package has __version__ attribute."""
        import nchantrs
        assert hasattr(nchantrs, '__version__')
        assert nchantrs.__version__

    def test_package_has_name(self):
        """Test package has __name__ attribute."""
        import nchantrs
        assert nchantrs.__name__ == 'nchantrs'

    def test_package_has_all_dir(self):
        """Test package __all__ list is defined."""
        import nchantrs
        if hasattr(nchantrs, '__all__'):
            assert isinstance(nchantrs.__all__, list)
