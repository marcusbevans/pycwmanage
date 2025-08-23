"""Pytest configuration file to load environment variables"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file before any tests run
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"Loaded environment variables from {env_path}")