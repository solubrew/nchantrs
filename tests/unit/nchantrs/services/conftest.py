"""Override the root conftest's session-scoped mock_pyqt for this subtree.

The root mock_pyqt hangs test execution (not collection).  The tags tests
don't need Qt, so override it with a no-op here.
"""
import pytest


@pytest.fixture(scope="session", autouse=True)
def mock_pyqt():
    """No-op override: tags tests don't require Qt mocking."""
    yield
