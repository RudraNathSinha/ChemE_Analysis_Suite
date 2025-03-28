import pytest
import os
import sys

# Add the application root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def test_image_path():
    """Fixture to provide path to test images"""
    return os.path.join(os.path.dirname(__file__), 'test_data', 'test_image.png')

@pytest.fixture
def test_data_path():
    """Fixture to provide path to test data files"""
    return os.path.join(os.path.dirname(__file__), 'test_data', 'test_data.csv')
