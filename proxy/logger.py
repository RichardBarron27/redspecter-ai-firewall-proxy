import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

DEFAULT_LOG_PATH = os.path.expanduser(
    "~/.redspecter_ai_firewall/logs/events.jsonl"
)

def ensure_log_dir(path: str = DEFAULT_LOG_PATH) -> Path:
    log_path = Path(path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    return log_path

def write_event(event: Dict[str, Any], path: str = DEFAULT_LOG_PATH) -> None:
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        **event,
    }
    log_path = ensure_log_dir(path)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
