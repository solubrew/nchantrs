"""Nchantrs Test Configuration and Fixtures.

This module provides pytest fixtures and configuration for testing
nchantrs applications. It uses the best practices from existing projects
in the workspace like goalt, mindot, and senbai.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Generator
from unittest.mock import MagicMock, patch

import pytest

# Add nchantrs to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock Qt before importing nchantrs modules that require Qt
QT_MOCK = pytest.fixture(scope="session", autouse=True)


def mock_qt_modules():
    """Create mock Qt modules to avoid GUI dependencies in tests."""
    mock_qt = MagicMock()
    mock_qt.QCoreApplication = MagicMock()
    mock_qt.QWidget = MagicMock()
    mock_qt.QMainWindow = MagicMock()
    mock_qt.QDialog = MagicMock()
    mock_qt.QApplication = MagicMock()
    mock_qt.Qt = MagicMock()
    mock_qt.Qt.WindowFlags = 0
    mock_qt.QSettings = MagicMock()
    mock_qt.QSettings.IniFormat = 1
    mock_qt.QDockWidget = MagicMock()
    mock_qt.QDockWidget.DockWidgetFloatable = 4
    return mock_qt


@pytest.fixture(scope="session", autouse=True)
def mock_pyqt():
    """Mock PyQt5/PySide6 modules to avoid GUI requirements in tests."""
    mock_qt = mock_qt_modules()
    
    qt_modules = {
        "PyQt5": mock_qt,
        "PyQt5.QtCore": mock_qt,
        "PyQt5.QtWidgets": mock_qt,
        "PyQt5.QtGui": mock_qt,
        "PySide6": mock_qt,
        "PySide6.QtCore": mock_qt,
        "PySide6.QtWidgets": mock_qt,
        "PySide6.QtGui": mock_qt,
        # nchantrs.libraries.pyqt imports many PySide6 submodules at
        # module-load time.  Mock them all so widgets can be imported
        # without a real PySide6 install.
        "PySide6.QtNetwork": mock_qt,
        "PySide6.QtSql": mock_qt,
        "PySide6.QtWebEngineWidgets": mock_qt,
        "PySide6.QtWebEngineCore": mock_qt,
        "PySide6.QtWebChannel": mock_qt,
        "PySide6.QtCharts": mock_qt,
        "PySide6.QtPrintSupport": mock_qt,
        "PySide6.QtPdfWidgets": mock_qt,
        "PySide6.QtPdf": mock_qt,
        "PySide6.QtSvg": mock_qt,
    }
    
    with patch.dict(sys.modules, qt_modules):
        yield mock_qt


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def temp_db_path(temp_dir: Path) -> Path:
    """Create a temporary database path."""
    return temp_dir / "test_nchantrs.db"


@pytest.fixture
def mock_app() -> MagicMock:
    """Create a mock application instance."""
    app = MagicMock()
    app.application_NCD = "test_app"
    app.model = MagicMock()
    app.model.slug = "test"
    app.model.store = MagicMock()
    app.model.store.EXTENSION = ".db"
    app.model.application_path = "/tmp/test_app"
    app.model.get_current_version = MagicMock(return_value="0.0.1")
    return app


@pytest.fixture
def mock_parent(mock_app: MagicMock) -> MagicMock:
    """Create a mock parent object with app reference."""
    parent = MagicMock()
    parent.app = mock_app
    return parent


@pytest.fixture
def sample_yaml_config() -> str:
    """Sample YAML configuration for testing."""
    return """
name: Test Application
version: 0.0.1
models:
  - name: TestModel
    fields:
      - name: id
        type: string
      - name: value
        type: integer
widgets:
  - type: button
    name: test_button
"""


@pytest.fixture
def sample_df_data() -> dict:
    """Sample dataframe data for testing utilities."""
    return {
        "pid_txt": ["0", "0", "1", "1"],
        "name_txt": ["Root", "Child1", "Grandchild1", "Grandchild2"],
        "UUID": ["uuid1", "uuid2", "uuid3", "uuid4"],
    }


@pytest.fixture
def mock_kahndor_config():
    """Mock kahndor.Instruct for testing without disk configs."""
    config = MagicMock()
    config.dikt = {
        "name_txt": "test_instance",
        "instance_id_txt": "test-instance-123",
        "instance_path_txt": "/tmp/test",
    }
    config.select = MagicMock(return_value=config)
    config.override = MagicMock(return_value=config)
    return config


# ================================================================================
# Pytest Configuration
# ================================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "integration: Integration tests for component interactions")
    config.addinivalue_line("markers", "slow: Tests that take longer to run")
    config.addinivalue_line("markers", "gui: Tests that require GUI components")
    config.addinivalue_line("markers", "database: Tests that require database")


# ================================================================================
# Test Data Factories
# ================================================================================

class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def create_instance_config(
        name: str = "test_instance",
        instance_id: str = "test-id-123",
        instance_path: str = "/tmp/test",
    ) -> dict:
        """Create a test instance configuration."""
        return {
            "name_txt": name,
            "instance_id_txt": instance_id,
            "instance_path_txt": instance_path,
        }
    
    @staticmethod
    def create_action_config(
        name: str = "test_action",
        code: str = "TEST",
        icon: str = "icon.png",
    ) -> dict:
        """Create a test action configuration."""
        return {
            "name_txt": name,
            "lookup_code_txt": code,
            "icon_txt": icon,
            "description_ltxt": f"Description for {name}",
            "shortcut_txt": "Ctrl+T",
            "tip_txt": f"Tip for {name}",
            "widget_txt": "test_widget",
            "params_dict": {},
        }
    
    @staticmethod
    def create_tree_node(
        name: str = "node",
        parent_id: str = "0",
        uuid: str = "node-uuid",
    ) -> dict:
        """Create a test tree node."""
        return {
            "name_txt": name,
            "pid_txt": parent_id,
            "UUID": uuid,
        }


@pytest.fixture
def factory() -> TestDataFactory:
    """Provide test data factory."""
    return TestDataFactory()


# ================================================================================
# Mock External Dependencies
# ================================================================================

@pytest.fixture(autouse=True)
def mock_external_dependencies():
    """Mock external dependencies that may not be available in test environment."""
    mocks = {
        "kahndor": MagicMock(),
        "kahndor.kahndor": MagicMock(),
        "squirl": MagicMock(),
        "squirl.orgnql": MagicMock(),
        "subtrix": MagicMock(),
        "pycurity": MagicMock(),
        "micromole": MagicMock(),
        "micromole.storage": MagicMock(),
    }
    
    with patch.dict("sys.modules", {k: v for k, v in mocks.items() if k not in sys.modules}):
        yield
