"""
Launcher script for Peenoise Language IDE GUI.
Usage:
    python run_gui.py
"""

import sys
import os

# Ensure the project root directory is in sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from gui_folder.app import main

if __name__ == "__main__":
    main()
