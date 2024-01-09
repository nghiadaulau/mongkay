import json
from applications.core.path_conf import ROOT_DIR

CONFIG = {}

try:
    with open(f"{ROOT_DIR}/config/config.json", "r") as f:
        CONFIG = json.load(f)
except Exception as e:
    print(f"Error to load config from {ROOT_DIR}/config/config.json")