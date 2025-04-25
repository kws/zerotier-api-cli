from platformdirs import user_config_dir
from pathlib import Path
import os
import yaml

CFG_DIR  = Path(user_config_dir("ztcli", "k-si.com"))    
CFG_FILE = CFG_DIR / "config.yaml"

def load_config():
    if CFG_FILE.exists():
        with open(CFG_FILE, "r") as f:
            return yaml.safe_load(f)
    return {}

def save_config(token: str, network_id: str):
    """Save ZeroTier configuration to file."""
    # Create config directory if it doesn't exist
    CFG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Prepare config data
    config = {
        "ZEROTIER_TOKEN": token,
        "ZEROTIER_NETWORK_ID": network_id
    }
    
    # Save to file
    with open(CFG_FILE, "w") as f:
        yaml.safe_dump(config, f)
    
    return CFG_FILE

def init_config():
    """Initialize configuration from file and environment."""
    cfg = load_config()
    for key, value in cfg.items():
        if key not in os.environ:
            os.environ[key] = str(value)
