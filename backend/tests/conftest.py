"""
TrustLens AI - Pytest Conftest Module
Ensures the project root directory is added to sys.path for backend package imports.
"""

import sys
import os

# Add project root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
