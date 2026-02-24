import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app, activities

@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities dict before each test to avoid state bleed."""
    for activity in activities.values():
        activity['participants'].clear()
