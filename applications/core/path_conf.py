import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define ROOT_DIR.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Define LOG_PATH for dir have log file.
LOG_PATH = f"{ROOT_DIR}/log"
