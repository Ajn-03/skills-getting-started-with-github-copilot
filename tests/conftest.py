import sys
import copy
import importlib.util
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Load the application module from src/app.py so tests operate on the same module instance
MODULE_NAME = "src.app"
SRC_PATH = Path(__file__).resolve().parents[1] / "src" / "app.py"

spec = importlib.util.spec_from_file_location(MODULE_NAME, str(SRC_PATH))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)
sys.modules[MODULE_NAME] = app_module

@pytest.fixture(scope="function", autouse=True)
def backup_activities():
    """Autouse fixture that backs up and restores `app_module.activities` around each test.

    This keeps tests deterministic by ensuring each test runs against the same
    initial in-memory data and any mutation is reverted after the test.
    """
    backup = copy.deepcopy(app_module.activities)
    yield
    # Restore original structure in-place so references stay valid
    app_module.activities.clear()
    app_module.activities.update(backup)

@pytest.fixture
def client():
    """Synchronous TestClient for the FastAPI `app` from src/app.py."""
    return TestClient(app_module.app)

@pytest.fixture
def app_module_fixture():
    """Expose the loaded app module to tests for assertions against in-memory state."""
    return app_module
