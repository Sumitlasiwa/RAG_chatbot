import pytest
import tempfile
from pathlib import Path

def test_load_txt_file():
    """Test loading a text file"""
    # Create a temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Hello World!\nTest Content")
        temp_file=f.name
        
